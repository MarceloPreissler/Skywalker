from __future__ import annotations

from bs4 import BeautifulSoup

from .. import schemas
from .base import BaseScraper, ScrapeResult, normalize_rate

_SAMPLE_HTML = """
<section id="plans">
  <article class="plan">
    <h2>Smart Edge 12</h2>
    <span class="term">12</span>
    <span class="rate">12.4¢/kWh</span>
    <span class="base">$9.95</span>
    <span class="cancel">$150</span>
    <span class="renewable">25%</span>
    <p class="features">Free nights from 8pm to 6am.</p>
  </article>
  <article class="plan">
    <h2>Flex Saver 24</h2>
    <span class="term">24</span>
    <span class="rate">11.1¢/kWh</span>
    <span class="base">$0</span>
    <span class="cancel">$295</span>
    <span class="renewable">30%</span>
    <p class="features">Bill credit after 1000 kWh.</p>
  </article>
</section>
"""


class TXUScraper(BaseScraper):
    provider_slug = "txu"

    def parse(self) -> ScrapeResult:
        soup = BeautifulSoup(_SAMPLE_HTML, "html.parser")
        plans = []
        for article in soup.select("section#plans article.plan"):
            plans.append(
                schemas.PlanCreate(
                    provider_id=0,
                    name=article.select_one("h2").get_text(strip=True),
                    term_months=int(article.select_one(".term").get_text(strip=True)),
                    rate_cents_kwh=normalize_rate(article.select_one(".rate").get_text()),
                    base_fee=float(article.select_one(".base").get_text(strip=True).replace("$", "")),
                    cancellation_fee=float(
                        article.select_one(".cancel").get_text(strip=True).replace("$", "")
                    ),
                    renewable_percentage=int(
                        article.select_one(".renewable").get_text(strip=True).replace("%", "")
                    ),
                    features=article.select_one(".features").get_text(strip=True),
                    url="https://www.txu.com/en/rates"
                )
            )

        provider = schemas.ProviderCreate(
            name="TXU Energy",
            slug=self.provider_slug,
            website="https://www.txu.com",
        )
        return ScrapeResult(provider=provider, plans=plans)
