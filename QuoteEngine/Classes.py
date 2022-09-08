from PIL import Image, ImageDraw, ImageFont
from abc import ABC, abstractmethod
from typing import List
import docx
import os
import pandas
import subprocess


class QuoteModel:
    def __init__(self, body, author):
        self.body = body
        self.author = author

    def __repr__(self):
        return f'<QuoteModel "{self.body}" by {self.author}>'


class IngestorInterface(ABC):
    @abstractmethod
    def can_ingest(cls, path) -> bool:
        pass

    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class IngestorInterCSV(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        df = pandas.read_csv(path, header=0)
        result = []
        for index, row in df.iterrows():
            body = row.body
            author = row.author
            quote = QuoteModel(body, author)
            result.append(quote)
        return result


class IngestorInterDOCX(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        doc = docx.Document(path)
        result = []
        for paragraph in doc.paragraphs:
            data = paragraph.text.strip()
            if not data:
                continue

            data = data.split(' - ')
            body = data[0].strip('"')
            author = data[1]
            quote = QuoteModel(body, author)
            result.append(quote)
        return result


class IngestorInterPDF(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        tmp = './tmp.txt'
        call = subprocess.call(['pdftotext', path, tmp])
        file_ref = open(tmp, "r")
        result = []
        for line in file_ref.readlines():
            line = line.strip('\n\r').strip()
            if len(line) > 0:
                data = line.split(' - ')
                body = data[0].strip('"')
                author = data[1]
                quote = QuoteModel(body, author)
                result.append(quote)
        file_ref.close()
        os.remove(tmp)
        return result


class IngestorInterTXT(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        result = []
        with open(path) as file:
            for line in file:
                data = line.strip()
                if not data:
                    continue

                data = data.split(' - ')
                body = data[0]
                author = data[1]
                quote = QuoteModel(body, author)
                result.append(quote)
        return result


class Ingestor(IngestorInterface):
    ingestors_map = {
        'csv': IngestorInterCSV,
        'docx': IngestorInterDOCX,
        'pdf': IngestorInterPDF,
        'txt': IngestorInterTXT,
    }

    @staticmethod
    def _extension(path) -> str:
        return path.split('.')[-1].lower()

    @classmethod
    def can_ingest(cls, path) -> bool:
        """Check if the path is an existent file and extension is allowed."""
        extension = cls._extension(path)
        return os.path.isfile(path) and extension in cls.ingestors_map.keys()

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise IOError(f"{path} cannot be ingested.")
        return cls.ingestors_map[cls._extension(path)].parse(path)


class MemeEngine():
    def __init__(self, output_path):
        self.output_path = output_path

    def make_meme(self, img_path, text, author, width=500) -> str:
        image = Image.open(img_path)

        font = ImageFont.truetype("./_data/fonts/LilitaOne-Regular.ttf", 20)
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), text, (0, 0, 0), font=font)

        font = ImageFont.truetype("./_data/fonts/LilitaOne-Regular.ttf", 16)
        draw = ImageDraw.Draw(image)
        draw.text((30, 40), '- ' + author, (0, 0, 0), font=font)

        output_path = self.output_path + '/' + img_path.split('/')[-1]
        image.save(output_path)

        return output_path
