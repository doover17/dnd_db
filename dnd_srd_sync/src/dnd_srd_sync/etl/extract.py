"""Extract data from the SRD API."""

from __future__ import annotations

from dnd_srd_sync.api.client import SrdClient


def extract_index(client: SrdClient) -> dict:
    """Fetch the API index payload."""
    response = client.get("/api")
    return response.json()
