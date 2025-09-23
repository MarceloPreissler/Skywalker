from __future__ import annotations

from bs4 import BeautifulSoup

from .. import schemas
from .base import BaseScraper, ScrapeResult

_SAMPLE_HTML = """
<table id="gexa-plans">
  <tr>
    <th>Plan</th><th>Term</th><th>Rate</th><th>Base Fee</th><th>Cancel Fee</th><th>Renewable</th><th>Features</th>
  </tr>
  <tr>
    <td>Gexa Saver Deluxe 12</td>
    <td>12</td>
    <td>9.8</td>
    <td>0</td>
    <td>150</td>
    <td>100</td>
    <td>100% renewable energy.</td>
  </tr>
  <tr>
    <td>Gexa Eco Saver 36</td>
    <td>36</td>
    <td>10.4</td>
    <td>5</td>
    <td>295</td>
    <td>100</td>
    <td>Bill credits and smart thermostat.</td>
  </tr>
</table>
"""


class GexaScraper(BaseScraper):
    provider_slug = "gexa"

    def parse(self) -> ScrapeResult:
        soup = BeautifulSoup(_SAMPLE_HTML, "html.parser")
        plans = []
        for row in soup.select("#gexa-plans tr")[1:]:
            cells = [col.get_text(strip=True) for col in row.find_all("td")]
            plans.append(
                schemas.PlanCreate(
                    provider_id=0,
                    name=cells[0],
                    term_months=int(cells[1]),
                    rate_cents_kwh=float(cells[2]) * 100,
                    base_fee=float(cells[3]),
                    cancellation_fee=float(cells[4]),
                    renewable_percentage=int(cells[5]),
                    features=cells[6],
                    url="https://www.gexaenergy.com/residential"
                )
            )

        provider = schemas.ProviderCreate(
            name="Gexa Energy",
            slug=self.provider_slug,
            website="https://www.gexaenergy.com",
        )
        return ScrapeResult(provider=provider, plans=plans)
