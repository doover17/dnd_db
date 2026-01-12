"""Transform SRD payloads into database-ready shapes."""

from __future__ import annotations

from typing import Iterable


def normalize_items(items: Iterable[dict]) -> list[dict]:
    """Normalize items from the API into a consistent dict shape."""
    normalized = []
    for item in items:
        normalized.append(
            {
                "index": item.get("index", ""),
                "name": item.get("name", ""),
                "url": item.get("url", ""),
            }
        )
    return normalized
