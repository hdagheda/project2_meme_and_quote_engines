from Ingestor.ingestor_interface import IngestorInterface
from typing import List
import zipfile
import xml.etree.ElementTree as ET
from QuoteEngine import QuoteModel
from Ingestor.common_functions import _line_to_quote


class DocxIngestor(IngestorInterface):
    """
    Ingest .docx (Word) files by extracting paragraph text and parsing lines into quotes.

    This implementation reads 'word/document.xml' from the .docx zip and collects all w:t text nodes.
    Each paragraph is treated as a potential 'quote - author' line.
    """
    allowed_extensions = {"docx"}

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
        with zipfile.ZipFile(path) as z:
            xml_bytes = z.read("word/document.xml")
        root = ET.fromstring(xml_bytes)

        # Namespaces used in WordprocessingML
        ns = {
            "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        }

        # For each paragraph (w:p), concatenate all text nodes (w:t)
        for p in root.findall(".//w:p", ns):
            texts = [t.text or "" for t in p.findall(".//w:t", ns)]
            paragraph = " ".join(t.strip() for t in texts if t is not None).strip()
            if not paragraph:
                continue
            q = _line_to_quote(paragraph)
            if q:
                quotes.append(q)

        return quotes
