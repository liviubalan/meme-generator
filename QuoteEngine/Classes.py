from PIL import Image, ImageDraw, ImageFont
from abc import ABC, abstractmethod
from typing import List
import docx
import os
import pandas
import random
import subprocess


class QuoteModel:
    def __init__(self, body, author):
        self.body = body
        self.author = author

    def __repr__(self):
        return f'<QuoteModel "{self.body}" by {self.author}>'


class IngestorInterface(ABC):
    @staticmethod
    def extension(path) -> str:
        return path.split('.')[-1].lower()

    @abstractmethod
    def can_ingest(cls, path) -> bool:
        pass

    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class IngestorInterCSV(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        return cls.extension(path) == 'csv'

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
        return cls.extension(path) == 'docx'

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
        return cls.extension(path) == 'pdf'

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
        return cls.extension(path) == 'txt'

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

    @classmethod
    def can_ingest(cls, path) -> bool:
        """Check if the path is an existent file and extension is allowed."""
        extension = cls.extension(path)
        return (
            os.path.isfile(path)
            and extension in cls.ingestors_map.keys()
            and cls.ingestors_map[extension].can_ingest(path)
        )

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise IOError(f"{path} cannot be ingested.")
        return cls.ingestors_map[cls.extension(path)].parse(path)


class MemeEngine():
    def __init__(self, output_path):
        self.output_path = output_path

    def make_meme(self, img_path, text, author, width=500) -> str:
        file = img_path.split('/')[-1]
        extension = file.split('.')[-1]
        if extension not in ['gif', 'jpg', 'png']:
            raise TypeError(f"File {img_path} is not a valid image.")
        image = Image.open(img_path)

        font = ImageFont.truetype("./_data/fonts/LilitaOne-Regular.ttf", 20)
        draw = ImageDraw.Draw(image)
        rand_x = random.randint(10, 50)
        rand_y = random.randint(10, 200)
        draw.text((rand_x, rand_y), text, '#FFF', font=font)

        font = ImageFont.truetype("./_data/fonts/LilitaOne-Regular.ttf", 16)
        draw = ImageDraw.Draw(image)
        coord = (rand_x + 20, rand_y + 30)
        draw.text(coord, '- ' + author, "#805500", font=font)

        image_width, image_height = image.size
        if image_width > width:
            new_size = (width, image_height * width // image_width)
            image = image.resize(new_size)

        output_path = self.output_path + '/' + file
        image.save(output_path)

        return output_path
