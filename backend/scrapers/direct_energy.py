from __future__ import annotations

from bs4 import BeautifulSoup

from .. import schemas
from .base import BaseScraper, ScrapeResult

_SAMPLE_HTML = """
<div class="carousel">
  <div class="slide" data-plan="Direct Better Rate 12" data-term="12" data-rate="11.9" data-base="0" data-cancel="150" data-renewable="25">
    <p>Online only plan with paperless billing.</p>
  </div>
  <div class="slide" data-plan="Direct Comfort 24" data-term="24" data-rate="12.5" data-base="4.95" data-cancel="295" data-renewable="30">
    <p>Includes HVAC maintenance visits.</p>
  </div>
</div>
"""


class DirectEnergyScraper(BaseScraper):
    provider_slug = "direct_energy"

    def parse(self) -> ScrapeResult:
        soup = BeautifulSoup(_SAMPLE_HTML, "html.parser")
        plans = []
        for slide in soup.select(".carousel .slide"):
            plans.append(
                schemas.PlanCreate(
                    provider_id=0,
                    name=slide["data-plan"],
                    term_months=int(slide["data-term"]),
                    rate_cents_kwh=float(slide["data-rate"]) * 100,
                    base_fee=float(slide["data-base"]),
                    cancellation_fee=float(slide["data-cancel"]),
                    renewable_percentage=int(slide["data-renewable"]),
                    features=slide.get_text(strip=True),
                    url="https://www.directenergy.com/texas"
                )
            )

        provider = schemas.ProviderCreate(
            name="Direct Energy",
            slug=self.provider_slug,
            website="https://www.directenergy.com",
        )
        return ScrapeResult(provider=provider, plans=plans)
