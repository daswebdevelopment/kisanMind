from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import text

from backend.database import engine

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {"status": "ok", "database": db_status}
