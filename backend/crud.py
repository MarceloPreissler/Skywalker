from typing import Iterable, List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from . import models, schemas


async def get_providers(session: AsyncSession) -> Sequence[models.Provider]:
    result = await session.execute(
        select(models.Provider)
        .options(selectinload(models.Provider.plans))
        .order_by(models.Provider.name)
    )
    return result.scalars().unique().all()


async def get_provider_by_slug(session: AsyncSession, slug: str) -> models.Provider | None:
    result = await session.execute(
        select(models.Provider).where(models.Provider.slug == slug)
    )
    return result.scalar_one_or_none()


async def get_plans_by_provider_slug(
    session: AsyncSession, slug: str
) -> Sequence[models.Plan]:
    result = await session.execute(
        select(models.Plan)
        .join(models.Provider)
        .options(selectinload(models.Plan.provider))
        .where(models.Provider.slug == slug)
    )
    return result.scalars().unique().all()


async def upsert_provider(session: AsyncSession, provider: schemas.ProviderCreate) -> models.Provider:
    existing = await get_provider_by_slug(session, provider.slug)
    if existing:
        existing.name = provider.name
        existing.website = provider.website
        await session.flush()
        return existing

    db_provider = models.Provider(**provider.model_dump())
    session.add(db_provider)
    await session.flush()
    return db_provider


async def list_plans(session: AsyncSession) -> Sequence[models.Plan]:
    result = await session.execute(
        select(models.Plan)
        .options(selectinload(models.Plan.provider))
        .order_by(models.Plan.rate_cents_kwh, models.Plan.term_months)
    )
    return result.scalars().unique().all()


async def get_plan(session: AsyncSession, plan_id: int) -> models.Plan | None:
    result = await session.execute(
        select(models.Plan)
            .options(selectinload(models.Plan.provider))
            .where(models.Plan.id == plan_id)
    )
    return result.scalar_one_or_none()


async def upsert_plans(
    session: AsyncSession,
    provider: models.Provider,
    plans: Iterable[schemas.PlanCreate],
) -> List[models.Plan]:
    """Replace provider plans with the supplied values."""

    existing_plans = await session.execute(
        select(models.Plan).where(models.Plan.provider_id == provider.id)
    )
    for db_plan in existing_plans.scalars().all():
        await session.delete(db_plan)

    created: List[models.Plan] = []
    for plan in plans:
        plan_data = plan.model_dump(exclude={"provider_id"})
        db_plan = models.Plan(provider_id=provider.id, **plan_data)
        session.add(db_plan)
        created.append(db_plan)

    await session.flush()
    return created
