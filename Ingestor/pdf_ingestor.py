import shutil
import subprocess
import tempfile
from typing import List

from Ingestor.common_functions import _line_to_quote
from Ingestor.ingestor_interface import IngestorInterface
from QuoteEngine import QuoteModel


class PDFIngestor(IngestorInterface):
    """
    Ingest .pdf files by leveraging the
    'pdftotext' utility if available on the system.

    - Requires 'pdftotext' to be installed and available in PATH.
    - Falls back to a clear error if the utility is not found.
    - Each resulting text line is parsed
      like a .txt line ('quote - author', etc.).
    """
    allowed_extensions = {"pdf"}

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        ext = cls._get_extension(path)
        return ext in cls.allowed_extensions

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            ext = cls._get_extension(path)
            raise ValueError(f"{cls.__name__} cannot ingest '*.{ext}' "
                             f"(path='{path}')")

        if shutil.which("pdftotext") is None:
            raise RuntimeError(
                "PDF ingestion requires the 'pdftotext' "
                "utility to be installed "
                "and available in PATH."
            )

        quotes: List[QuoteModel] = []
        with tempfile.NamedTemporaryFile(
                suffix=".txt",
                delete=True
        ) as tmp_out:
            # Convert PDF to text
            subprocess.run(
                ["pdftotext", "-layout", path, tmp_out.name],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            tmp_out.seek(0)
            text = tmp_out.read().decode("utf-8", errors="ignore")

        for line in text.splitlines():
            q = _line_to_quote(line)
            if q:
                quotes.append(q)

        return quotes
