from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from .config import get_settings
from .database import AsyncSessionLocal
from .scrapers.runner import initialize_database, run_scraper

scheduler: AsyncIOScheduler | None = None


async def run_all_scrapers() -> None:
    settings = get_settings()
    async with AsyncSessionLocal() as session:
        for slug in settings.scrape_providers:
            logger.info("Running scraper for {slug}", slug=slug)
            await run_scraper(session, slug)


async def schedule_jobs() -> None:
    global scheduler
    settings = get_settings()
    if not settings.scheduler_enabled:
        return

    await initialize_database()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_all_scrapers,
        trigger=IntervalTrigger(minutes=settings.scrape_interval_minutes),
        id="scrape-job",
        replace_existing=True,
    )
    scheduler.start()


async def shutdown_scheduler() -> None:
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown()
        scheduler = None
