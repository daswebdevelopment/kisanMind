from __future__ import annotations

import os

from fastapi import APIRouter, Query as FastAPIQuery, Response

from backend.database import SessionLocal
from backend.models.farmer import Farmer
from backend.models.query import Query
from backend.services.ai_service import generate_farmer_answer
from backend.services.whatsapp import send_whatsapp_message

router = APIRouter(prefix="/webhook", tags=["webhook"])

FALLBACK_MESSAGE = (
    "Maafi kijiye, abhi technical samasya hai. "
    "Thodi der baad dobara try karein. 🙏"
)


@router.get("/whatsapp")
def verify_whatsapp_webhook(
    hub_mode: str | None = FastAPIQuery(default=None, alias="hub.mode"),
    hub_verify_token: str | None = FastAPIQuery(default=None, alias="hub.verify_token"),
    hub_challenge: str | None = FastAPIQuery(default=None, alias="hub.challenge"),
):
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "kisanmind-verify-token")

    if hub_mode == "subscribe" and hub_verify_token == verify_token and hub_challenge:
        return Response(content=hub_challenge, media_type="text/plain", status_code=200)
    return Response(content="verification failed", media_type="text/plain", status_code=403)


@router.post("/whatsapp")
def receive_whatsapp_webhook(payload: dict) -> dict[str, str]:
    try:
        entries = payload.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])

                for message in messages:
                    if message.get("type") != "text":
                        continue

                    phone_number = message.get("from")
                    text = message.get("text", {}).get("body", "").strip()

                    if not phone_number or not text:
                        continue

                    db = SessionLocal()
                    try:
                        farmer = db.query(Farmer).filter(Farmer.phone_number == phone_number).first()
                        if farmer is None:
                            farmer = Farmer(
                                name=f"Farmer {phone_number[-4:]}",
                                phone_number=phone_number,
                                state="unknown",
                                district="unknown",
                                preferred_language="hindi",
                            )
                            db.add(farmer)
                            db.flush()

                        query = Query(
                            farmer_id=farmer.id,
                            question=text,
                            answer=None,
                            language="en",
                            source="whatsapp",
                        )
                        db.add(query)
                        db.flush()

                        try:
                            answer = generate_farmer_answer(text)
                        except Exception:
                            answer = FALLBACK_MESSAGE

                        query.answer = answer
                        db.commit()
                    except Exception:
                        db.rollback()
                        answer = FALLBACK_MESSAGE
                    finally:
                        db.close()

                    send_whatsapp_message(phone_number, answer)
    except Exception:
        pass

    return {"status": "received"}
