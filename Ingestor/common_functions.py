from QuoteEngine import QuoteModel


def _line_to_quote(line: str) -> QuoteModel | None:
    """
    Try to parse a single line of text into a QuoteModel
    using common separators. Returns None if the line can't
    be parsed into (body, author).
    """
    if not line:
        return None
    s = line.strip()
    if not s or s.startswith("#"):
        return None

    separators = (" - ", " — ", "–", "—", "-", ",", "|", ";")
    for sep in separators:
        if sep in s:
            left, right = s.split(sep, 1)
            body = left.strip().strip('"').strip("'")
            author = right.strip().strip('"').strip("'")
            if body and author:
                try:
                    return QuoteModel(body=body, author=author)
                except ValueError:
                    return None
    return None
