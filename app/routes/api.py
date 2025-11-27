from fastapi import APIRouter, Request, UploadFile, File, Form
from pydantic import BaseModel
from pathlib import Path
from uuid import uuid4

from ..db import SessionLocal
from ..models import Event

UPLOAD_DIR = Path("data/uploads/cv")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


router = APIRouter()

class TrackEvent(BaseModel):
    event_name: str
    page: str
    variant: str | None = None
    metadata: dict | None = None

class ContactForm(BaseModel):
    nombre: str
    apellido: str
    email: str
    carrera: str
    iniciativa: str | None = None
    archivo_nombre: str | None = None

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

@router.post("/contact-upload")
async def contact_upload(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    carrera: str = Form(...),
    iniciativa: str = Form(""),
    archivo: UploadFile | None = File(None),
):
    """
    Recibe el formulario de contacto + archivo y:

    - guarda el CV en disco (data/uploads/cv)
    - registra un evento 'contact_form_submitted' en la tabla events
      con todos los datos en metadata (incluyendo ruta del archivo)
    """

    archivo_nombre = None
    archivo_path = None

    if archivo is not None and archivo.filename:
        archivo_nombre = archivo.filename

        # extensión original (ej: .pdf)
        ext = Path(archivo.filename).suffix

        # nombre único para evitar colisiones y no exponer el nombre original
        unique_name = f"{uuid4().hex}{ext}"

        full_path = UPLOAD_DIR / unique_name

        # guardamos el archivo en disco
        contents = await archivo.read()
        full_path.write_bytes(contents)

        archivo_path = str(full_path)

    # Armamos el metadata que se guarda en la columna JSON `metadata`
    metadata = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "carrera": carrera,
        "iniciativa": iniciativa,
        "archivo_nombre": archivo_nombre,
        "archivo_path": archivo_path,
    }

    # Reutilizamos el endpoint de analytics
    event = TrackEvent(
        event_name="contact_form_submitted",
        page=request.headers.get("referer") or "/",
        metadata=metadata,
    )

    # Esto guarda el evento en la tabla `events`
    return await track(event, request)


@router.post("/contact")
async def contact(form: ContactForm, request: Request):
    """
    Recibe los datos del formulario de contacto y los guarda
    como un evento en la tabla 'events'.
    """
    # Armamos un TrackEvent reutilizando la lógica existente
    event = TrackEvent(
        event_name="contact_form_submitted",
        page=request.headers.get("referer") or "/",
        metadata=form.dict(),
    )

    # Reutilizamos el endpoint de tracking existente
    return await track(event, request)
