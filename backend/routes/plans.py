from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, schemas
from ..database import get_session

router = APIRouter(prefix="/plans", tags=["plans"])


BENCHMARK_PROVIDER_SLUG = "txu"
BENCHMARK_USAGE_KWH = 1000


def _select_benchmark_plan(
    plans: Sequence[models.Plan], usage_kwh: float
) -> models.Plan | None:
    eligible = [plan for plan in plans if plan.rate_cents_kwh is not None]
    if not eligible:
        return None
    return min(eligible, key=lambda candidate: candidate.cost_for_usage(usage_kwh))


def _benchmark_against_txu(
    plan: models.Plan, txu_plan: models.Plan, usage_kwh: float
) -> float | None:
    if plan.rate_cents_kwh is None or txu_plan.rate_cents_kwh is None:
        return None
    return txu_plan.cost_for_usage(usage_kwh) - plan.cost_for_usage(usage_kwh)


@router.get("", response_model=Sequence[schemas.PlanRead])
async def list_plans(session: AsyncSession = Depends(get_session)):
    plans = await crud.list_plans(session)
    txu_plans = [
        plan
        for plan in plans
        if plan.provider and plan.provider.slug == BENCHMARK_PROVIDER_SLUG
    ]
    benchmark = _select_benchmark_plan(txu_plans, BENCHMARK_USAGE_KWH)

    enriched: list[schemas.PlanRead] = []
    for plan in plans:
        savings = (
            _benchmark_against_txu(plan, benchmark, BENCHMARK_USAGE_KWH)
            if benchmark
            else None
        )
        plan_read = schemas.PlanRead.model_validate(plan, from_attributes=True)
        enriched.append(plan_read.model_copy(update={"estimated_savings_vs_txu": savings}))
    return enriched


@router.get("/{plan_id}", response_model=schemas.PlanRead)
async def read_plan(plan_id: int, session: AsyncSession = Depends(get_session)):
    plan = await crud.get_plan(session, plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    txu_plans = await crud.get_plans_by_provider_slug(session, BENCHMARK_PROVIDER_SLUG)
    benchmark = _select_benchmark_plan(txu_plans, BENCHMARK_USAGE_KWH)
    savings = (
        _benchmark_against_txu(plan, benchmark, BENCHMARK_USAGE_KWH) if benchmark else None
    )
    plan_read = schemas.PlanRead.model_validate(plan, from_attributes=True)
    return plan_read.model_copy(update={"estimated_savings_vs_txu": savings})
