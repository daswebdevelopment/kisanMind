from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base, UUIDPrimaryKeyMixin


class Crop(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "crops"

    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    crop_name: Mapped[str] = mapped_column(String(100), nullable=False)
    sowing_date: Mapped[date] = mapped_column(Date, nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    farmer = relationship("Farmer", back_populates="crops")
