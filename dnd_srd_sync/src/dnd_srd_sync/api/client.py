"""HTTP client for SRD API."""

from __future__ import annotations

from dataclasses import dataclass

import httpx
from tenacity import Retrying, stop_after_attempt, wait_exponential

from dnd_srd_sync.config import Settings


@dataclass(slots=True)
class SrdClient:
    """Client for SRD API requests."""

    base_url: str
    request_timeout_secs: int
    retry_max_attempts: int

    @classmethod
    def from_settings(cls, settings: Settings) -> "SrdClient":
        return cls(
            base_url=settings.api_base_url,
            request_timeout_secs=settings.request_timeout_secs,
            retry_max_attempts=settings.retry_max_attempts,
        )

    def get(self, path: str) -> httpx.Response:
        """GET a resource from the SRD API."""
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        retrying = Retrying(
            stop=stop_after_attempt(self.retry_max_attempts),
            wait=wait_exponential(multiplier=1, min=1, max=8),
            reraise=True,
        )
        for attempt in retrying:
            with attempt:
                with httpx.Client(timeout=self.request_timeout_secs) as client:
                    response = client.get(url)
                    response.raise_for_status()
                    return response
        raise RuntimeError("Retrying did not execute any attempts.")
