from fastapi import APIRouter, Request
from pydantic import BaseModel
from pathlib import Path

from ..db import SessionLocal
from ..models import Event

router = APIRouter()

class TrackEvent(BaseModel):
    event_name: str
    page: str
    variant: str | None = None
    metadata: dict | None = None

@router.post("/track")
async def track(event: TrackEvent, request: Request):
    """First-party analytics endpoint: stores interaction events.

    - `event_name` is treated as an opaque identifier and stored as-is
      (e.g. "click_buy-now_hero"). Any parsing is done later, outside this API.
    - `variant` may be provided by the client or injected via middleware
      into `request.state.variant`.
    """
    db = SessionLocal()
    try:
        session_id = getattr(request.state, "session_id", None)
        variant = event.variant or getattr(request.state, "variant", None)
        metadata = event.metadata or {}

        ev = Event(
            session_id=session_id,
            event_name=event.event_name,
            page_url=event.page,
            variant_name=variant,
            event_metadata=metadata,
            referrer=request.headers.get("referer"),
            user_agent=request.headers.get("user-agent"),
        )
        db.add(ev)
        db.commit()
    finally:
        db.close()

    return {"status": "ok"}
