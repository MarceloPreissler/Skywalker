from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
from ..database import get_session

router = APIRouter(prefix="/plans", tags=["plans"])


@router.get("", response_model=Sequence[schemas.PlanRead])
async def list_plans(session: AsyncSession = Depends(get_session)):
    plans = await crud.list_plans(session)
    return plans


@router.get("/{plan_id}", response_model=schemas.PlanRead)
async def read_plan(plan_id: int, session: AsyncSession = Depends(get_session)):
    plan = await crud.get_plan(session, plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return plan
