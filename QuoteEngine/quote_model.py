# Python
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class QuoteModel:
    """
    A simple value object representing a quote.

    Attributes:
        body: The text of the quote.
        author: The author of the quote.
    """
    body: str
    author: str

    def __post_init__(self):
        body = (self.body or "").strip()
        author = (self.author or "").strip()
        if not body:
            raise ValueError("Quote body must not be empty")
        if not author:
            raise ValueError("Quote author must not be empty")
        # Workaround for frozen dataclass to store normalized values
        object.__setattr__(self, "body", body)
        object.__setattr__(self, "author", author)

    def __str__(self) -> str:
        return f'"{self.body}" - {self.author}'

    def __repr__(self) -> str:
        return f"QuoteModel(body={self.body!r}, author={self.author!r})"
