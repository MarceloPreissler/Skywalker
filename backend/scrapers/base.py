from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup

from .. import schemas


@dataclass
class ScrapeResult:
    provider: schemas.ProviderCreate
    plans: List[schemas.PlanCreate]


class BaseScraper:
    """Common scraper utilities."""

    provider_slug: str

    def fetch_html(self, url: str) -> BeautifulSoup:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def parse(self) -> ScrapeResult:  # pragma: no cover - to be implemented by subclasses
        raise NotImplementedError


def normalize_rate(value: str) -> float | None:
    try:
        cleaned = value.replace("$", "").replace("¢", "").replace("/kWh", "").strip()
        if not cleaned:
            return None
        return float(cleaned) * (100 if "¢" not in value and "c" not in value.lower() else 1)
    except ValueError:
        return None


def text_or_none(element) -> str | None:
    if element is None:
        return None
    text = element.get_text(strip=True)
    return text or None
