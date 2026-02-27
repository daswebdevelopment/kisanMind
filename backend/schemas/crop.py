from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class CropBase(BaseModel):
    farmer_id: UUID
    crop_name: str
    sowing_date: date
    state: str
    district: str
    status: str


class CropCreate(CropBase):
    pass


class CropRead(CropBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
