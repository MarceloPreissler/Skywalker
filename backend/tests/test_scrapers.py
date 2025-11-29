import pytest

from backend.scrapers.direct_energy import DirectEnergyScraper
from backend.scrapers.gexa import GexaScraper
from backend.scrapers.reliant import ReliantScraper
from backend.scrapers.txu import TXUScraper


@pytest.mark.parametrize(
    "scraper_cls",
    [TXUScraper, ReliantScraper, GexaScraper, DirectEnergyScraper],
)
def test_scraper_returns_plans(scraper_cls):
    scraper = scraper_cls()
    result = scraper.parse()
    assert result.provider.slug
    assert result.plans
    for plan in result.plans:
        assert plan.name
        assert plan.rate_cents_kwh is not None
