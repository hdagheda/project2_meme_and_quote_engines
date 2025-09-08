from Ingestor.ingestor_interface import IngestorInterface
from Ingestor.common_functions import _line_to_quote
from typing import List

from QuoteEngine import QuoteModel


class TextIngestor(IngestorInterface):
    """
    Ingest .txt files where each non-empty, non-comment line contains a quote and author
    separated by a common delimiter (e.g., ' - ', '-', ',', '|', ';').
    """
    allowed_extensions = {"txt"}

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        ext = cls._get_extension(path)
        return ext in cls.allowed_extensions

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            ext = cls._get_extension(path)
            raise ValueError(f"{cls.__name__} cannot ingest '*.{ext}' (path='{path}')")

        quotes: List[QuoteModel] = []
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                q = _line_to_quote(raw_line)
                if q:
                    quotes.append(q)
        return quotes
