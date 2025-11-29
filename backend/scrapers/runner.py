from __future__ import annotations

from typing import Dict, Iterable, List

from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
from ..models import Base
from ..database import engine
from .base import ScrapeResult
from .direct_energy import DirectEnergyScraper
from .gexa import GexaScraper
from .reliant import ReliantScraper
from .txu import TXUScraper

SCRAPER_REGISTRY = {
    "txu": TXUScraper,
    "reliant": ReliantScraper,
    "gexa": GexaScraper,
    "direct_energy": DirectEnergyScraper,
}


async def run_scraper(session: AsyncSession, slug: str) -> ScrapeResult:
    scraper_cls = SCRAPER_REGISTRY.get(slug)
    if not scraper_cls:
        raise ValueError(f"Unknown provider slug: {slug}")

    scraper = scraper_cls()
    result = scraper.parse()
    provider = await crud.upsert_provider(session, result.provider)

    normalized_plans: List[schemas.PlanCreate] = []
    for plan in result.plans:
        normalized_plans.append(
            schemas.PlanCreate(
                provider_id=provider.id,
                name=plan.name,
                term_months=plan.term_months,
                rate_cents_kwh=plan.rate_cents_kwh,
                base_fee=plan.base_fee,
                cancellation_fee=plan.cancellation_fee,
                renewable_percentage=plan.renewable_percentage,
                features=plan.features,
                url=plan.url,
            )
        )

    await crud.upsert_plans(session, provider, normalized_plans)
    await session.commit()
    return result


async def initialize_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
