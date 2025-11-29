from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    website: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    plans: Mapped[List["Plan"]] = relationship(
        back_populates="provider",
        cascade="all, delete-orphan",
    )


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    term_months: Mapped[int | None] = mapped_column(Integer)
    rate_cents_kwh: Mapped[float | None] = mapped_column(Float)
    base_fee: Mapped[float | None] = mapped_column(Float)
    cancellation_fee: Mapped[float | None] = mapped_column(Float)
    renewable_percentage: Mapped[int | None] = mapped_column(Integer)
    features: Mapped[str | None] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(String(255))
    last_scraped_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    provider: Mapped[Provider] = relationship(back_populates="plans")

    def cost_for_usage(self, usage_kwh: float) -> float:
        """Estimate the monthly cost for a given energy usage."""

        rate_cents = self.rate_cents_kwh or 0.0
        base_fee = self.base_fee or 0.0
        return base_fee + (rate_cents / 100.0) * usage_kwh
