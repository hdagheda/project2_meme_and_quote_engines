from Ingestor.ingestor_interface import IngestorInterface
import csv
from typing import List

from QuoteEngine import QuoteModel


class CSVIngestor(IngestorInterface):
    """
    Ingest .csv files into QuoteModel objects.

    Supports:
      - Headers: body, author (case-insensitive). If present, uses DictReader.
      - No headers: expects two columns [body, author].
    """
    allowed_extensions = {"csv"}

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
        with open(path, "r", encoding="utf-8", newline="") as f:
            # Peek the first line to detect header presence
            first_pos = f.tell()
            first_line = f.readline()
            f.seek(first_pos)

            has_header = False
            if first_line:
                lowered = [h.strip().lower() for h in first_line.split(",")]
                has_header = ("body" in lowered and "author" in lowered) or ("quote" in lowered and "author" in lowered)

            if has_header:
                reader = csv.DictReader(f)
                for row in reader:
                    body = (row.get("body") or row.get("quote") or "").strip()
                    author = (row.get("author") or "").strip()
                    if not body and not author:
                        continue
                    try:
                        quotes.append(QuoteModel(body=body, author=author))
                    except ValueError:
                        continue
            else:
                reader = csv.reader(f)
                for parts in reader:
                    if not parts or len(parts) < 2:
                        continue
                    body = (parts[0] or "").strip()
                    author = (parts[1] or "").strip()
                    if not body and not author:
                        continue
                    try:
                        quotes.append(QuoteModel(body=body, author=author))
                    except ValueError:
                        continue
        return quotes
