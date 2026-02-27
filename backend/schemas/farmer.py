from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FarmerBase(BaseModel):
    name: str
    phone_number: str
    state: str
    district: str
    preferred_language: str = "hindi"


class FarmerCreate(FarmerBase):
    pass


class FarmerRead(FarmerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
