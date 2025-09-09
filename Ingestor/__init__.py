# Python
"""
Ingestor package public API and default helper registration.
"""

from .ingestor import Ingestor
# ... existing code ...
from .text_ingestor import TextIngestor
from .csv_ingestor import CSVIngestor
from .docx_ingestor import DocxIngestor
from .pdf_ingestor import PDFIngestor

# Register default helper ingestors so the facade can handle common formats.
Ingestor.register_many([TextIngestor, CSVIngestor, DocxIngestor, PDFIngestor])

__all__ = [
    "Ingestor",
    "TextIngestor",
    "CSVIngestor",
    "DocxIngestor",
    "PDFIngestor",
]
