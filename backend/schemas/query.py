from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class QueryBase(BaseModel):
    farmer_id: UUID
    question: str
    answer: str | None = None
    language: str
    source: str


class QueryCreate(QueryBase):
    pass


class QueryRead(QueryBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
