from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class PlanBase(BaseModel):
    name: str
    term_months: Optional[int] = None
    rate_cents_kwh: Optional[float] = Field(None, description="Rate in cents per kWh")
    base_fee: Optional[float] = None
    cancellation_fee: Optional[float] = None
    renewable_percentage: Optional[int] = None
    features: Optional[str] = None
    url: Optional[str] = None


class PlanCreate(PlanBase):
    provider_id: int


class PlanUpdate(BaseModel):
    rate_cents_kwh: Optional[float] = None
    base_fee: Optional[float] = None
    cancellation_fee: Optional[float] = None
    renewable_percentage: Optional[int] = None
    features: Optional[str] = None


class PlanRead(PlanBase):
    id: int
    provider_id: int
    last_scraped_at: datetime
    estimated_savings_vs_txu: Optional[float] = Field(
        default=None, description="Estimated monthly savings compared to TXU"
    )

    model_config = ConfigDict(from_attributes=True)


class ProviderBase(BaseModel):
    name: str
    slug: str
    website: Optional[str] = None


class ProviderCreate(ProviderBase):
    pass


class ProviderRead(ProviderBase):
    id: int
    created_at: datetime
    plans: List[PlanRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
