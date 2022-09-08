from abc import ABC, abstractmethod
from typing import List


class QuoteModel:
    def __init__(self, body, author):
        self.body = body
        self.author = author


class IngestorInterface(ABC):
    @abstractmethod
    def can_ingest(cls, path) -> bool:
        pass

    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class Ingestor(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class IngestorInterCSV(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class IngestorInterDOCX(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class IngestorInterPDF(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class IngestorInterTXT(IngestorInterface):
    @classmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class MemeEngine():
    def __init__(self, path):
        self.path = path
