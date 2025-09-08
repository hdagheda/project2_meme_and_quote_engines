# Python
from __future__ import annotations

from typing import Any, ClassVar, Iterable, Optional, Set, Type

from QuoteEngine.quote_model import QuoteModel
from typing import List
from Ingestor.ingestor_interface import IngestorInterface

import zipfile
import xml.etree.ElementTree as ET
import tempfile
import subprocess
import shutil


class Ingestor(IngestorInterface):
    """
    Final façade for ingestion that encapsulates helper ingestors.

    - Register concrete helpers (subclasses of IngestorInterface) via register/register_many.
    - Ingestor.can_ingest(path) returns True if any helper supports the file.
    - Ingestor.parse(path) delegates to the first matching helper.
    """

    _helpers: ClassVar[List[Type[IngestorInterface]]] = []
    # Union of all registered helpers' extensions (informational)
    allowed_extensions: ClassVar[Set[str]] = set()

    @classmethod
    def register(cls, helper: Type[IngestorInterface]) -> None:
        """
        Register a helper ingestor.

        The helper must subclass IngestorInterface and define non-empty allowed_extensions.
        """
        if not isinstance(helper, type) or not issubclass(helper, IngestorInterface):
            raise TypeError("Helper must be a subclass of IngestorInterface")

        if helper in cls._helpers:
            return

        exts = getattr(helper, "allowed_extensions", None)
        if not exts:
            raise ValueError(f"{helper.__name__} must define non-empty allowed_extensions")

        cls._helpers.append(helper)
        cls.allowed_extensions.update(exts)

    @classmethod
    def register_many(cls, helpers: Iterable[Type[IngestorInterface]]) -> None:
        """Register multiple helper ingestors at once."""
        for h in helpers:
            cls.register(h)

    @classmethod
    def clear_helpers(cls) -> None:
        """Remove all registered helpers (useful for tests/reconfiguration)."""
        cls._helpers.clear()
        cls.allowed_extensions.clear()

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Return True if any registered helper can handle the given path.
        """
        for helper in cls._helpers:
            if helper.can_ingest(path):
                return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[Any]:
        """
        Delegate parsing to the first registered helper that supports the file.

        Raises:
            RuntimeError: If no helpers are registered.
            ValueError: If no helper supports the given file type.
        """
        if not cls._helpers:
            raise RuntimeError(
                "No ingestor helpers registered. Register helpers with Ingestor.register(...)"
            )

        helper = cls._select_helper(path)
        if helper is None:
            ext = cls._get_extension(path)
            raise ValueError(f"No registered ingestor supports '*.{ext}' files (path='{path}')")

        return helper.parse(path)

    @classmethod
    def _select_helper(cls, path: str) -> Optional[Type[IngestorInterface]]:
        """Return the first registered helper that can handle the path, if any."""
        for helper in cls._helpers:
            if helper.can_ingest(path):
                return helper
        return None
