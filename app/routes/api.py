from fastapi import APIRouter, Request
from pydantic import BaseModel
from ..db import SessionLocal
from ..models import Event, UniversityQuote

router = APIRouter()

class TrackEvent(BaseModel):
    event_name: str
    page: str
    variant: str | None = None
    metadata: dict | None = None

@router.post("/track")
async def track(event: TrackEvent, request: Request):
    """First-party analytics endpoint: stores interaction events.

    Events are associated with the anonymous session and current A/B variant.
    """
    db = SessionLocal()
    session_id = getattr(request.state, "session_id", None)
    variant = event.variant or getattr(request.state, "variant", None)

    ev = Event(
        session_id=session_id,
        event_name=event.event_name,
        page_url=event.page,
        variant_name=variant,
        event_metadata=event.metadata,
        referrer=request.headers.get("referer"),
        user_agent=request.headers.get("user-agent"),
    )
    db.add(ev)
    db.commit()
    db.close()
    return {"status": "ok"}


class UniversityQuoteForm(BaseModel):
    institution_name: str
    country: str
    quantity: int
    timeframe: str
    contact_email: str

@router.post("/university-quote")
async def university_quote(form: UniversityQuoteForm, request: Request):
    """Handles university quote requests.

    Data is stored in the database; you can later add email notifications.
    """
    db = SessionLocal()
    quote = UniversityQuote(**form.dict())
    db.add(quote)
    db.commit()
    db.close()
    return {"status": "ok"}
