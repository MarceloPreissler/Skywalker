from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
from ..database import get_session

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=Sequence[schemas.ProviderRead])
async def list_providers(session: AsyncSession = Depends(get_session)):
    providers = await crud.get_providers(session)
    return providers
