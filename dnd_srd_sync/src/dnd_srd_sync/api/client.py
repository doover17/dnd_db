"""HTTP client for SRD API."""

from __future__ import annotations

from dataclasses import dataclass

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from dnd_srd_sync.config import Settings


@dataclass(slots=True)
class SrdClient:
    """Client for SRD API requests."""

    base_url: str

    @classmethod
    def from_settings(cls, settings: Settings) -> "SrdClient":
        return cls(base_url=settings.api_base_url)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
    def get(self, path: str) -> httpx.Response:
        """GET a resource from the SRD API."""
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            return response
