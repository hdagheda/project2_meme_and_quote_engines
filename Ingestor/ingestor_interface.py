# Python
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar, Iterable, List
import os


class IngestorInterface(ABC):
    """
    Abstract interface for file ingestors.

    Subclasses should:
      - Set allowed_extensions to the set of supported file extensions.
      - Implement parse() to return a list of parsed quote-like objects.
    """

    allowed_extensions: ClassVar[set[str]] = set()

    @classmethod
    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Check whether this ingestor can handle the given file path
        based on the file extension.
        """
        ext = cls._get_extension(path)
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[Any]:
        """
        Parse the given file and return a list of domain objects
        (e.g., quotes). Must be implemented by subclasses.
        """
        raise NotImplementedError

    @staticmethod
    def _get_extension(path: str) -> str:
        """
        Extract lowercase file extension without the dot, e.g., 'csv'.
        """
        _, ext = os.path.splitext(path or "")
        return ext.replace(".", "").lower()
