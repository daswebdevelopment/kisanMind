from __future__ import annotations

from fastapi import FastAPI

from backend.database import engine
from backend.models.base import Base
from backend import models  # noqa: F401
from backend.routes.health import router as health_router
from backend.routes.webhook import router as webhook_router

app = FastAPI(title="KisanMind API")


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(webhook_router)
