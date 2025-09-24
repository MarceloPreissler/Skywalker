from __future__ import annotations

from bs4 import BeautifulSoup

from .. import schemas
from .base import BaseScraper, ScrapeResult, normalize_rate

_SAMPLE_HTML = """
<ul class="plans">
  <li>
    <h3>Reliant Secure Advantage 12</h3>
    <div class="details" data-term="12" data-rate="10.9" data-base="4.95" data-cancel="150" data-renewable="20">
      <p>Fixed rate with autopay discount.</p>
    </div>
  </li>
  <li>
    <h3>Reliant Truly Free Weekends</h3>
    <div class="details" data-term="24" data-rate="12.3" data-base="9.95" data-cancel="295" data-renewable="15">
      <p>Free energy every weekend.</p>
    </div>
  </li>
</ul>
"""


class ReliantScraper(BaseScraper):
    provider_slug = "reliant"

    def parse(self) -> ScrapeResult:
        soup = BeautifulSoup(_SAMPLE_HTML, "html.parser")
        plans = []
        for details in soup.select(".plans .details"):
            rate = float(details["data-rate"]) * 100
            plans.append(
                schemas.PlanCreate(
                    provider_id=0,
                    name=details.parent.select_one("h3").get_text(strip=True),
                    term_months=int(details["data-term"]),
                    rate_cents_kwh=rate,
                    base_fee=float(details["data-base"]),
                    cancellation_fee=float(details["data-cancel"]),
                    renewable_percentage=int(details["data-renewable"]),
                    features=details.get_text(strip=True),
                    url="https://www.reliant.com/en/plans"
                )
            )

        provider = schemas.ProviderCreate(
            name="Reliant Energy",
            slug=self.provider_slug,
            website="https://www.reliant.com",
        )
        return ScrapeResult(provider=provider, plans=plans)
