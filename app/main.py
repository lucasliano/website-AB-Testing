import random
import uuid

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from .config import settings
from .db import Base, engine, SessionLocal
from .models import ABAssignment, PageView
from .routes import pages, api

VARIANTS = ["hero_A", "hero_B"]


def init_db():
    """Initialize database tables on startup.

    For a larger project you would use Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)


class SessionVariantMiddleware(BaseHTTPMiddleware):
    """Assigns an anonymous session ID and an A/B test variant.

    - If the visitor has no `session_id` cookie, a UUID is created.
    - If the visitor has no `ab_variant` cookie, one is chosen randomly.
    - Page views are logged along with the chosen variant.

    This middleware is intentionally simple and self-contained so the
    A/B mechanism is easy to understand and maintain.
    """

    async def dispatch(self, request: Request, call_next):
        response: Response

        session_id = request.cookies.get(settings.COOKIE_SESSION_NAME)
        variant = request.cookies.get(settings.COOKIE_VARIANT_NAME)

        db = SessionLocal()

        # Create a new anonymous session if needed
        if not session_id:
            session_id = str(uuid.uuid4())

        # Assign an A/B variant if not already set
        if not variant:
            variant = random.choice(VARIANTS)
            assignment = ABAssignment(session_id=session_id, variant_name=variant)
            db.add(assignment)
            db.commit()

        # Store on request state for use in routes/templates
        request.state.session_id = session_id
        request.state.variant = variant

        response = await call_next(request)

        # Set cookies so the browser persists session + variant
        response.set_cookie(
            settings.COOKIE_SESSION_NAME,
            session_id,
            httponly=True,
            samesite="lax",
        )
        response.set_cookie(
            settings.COOKIE_VARIANT_NAME,
            variant,
            httponly=False,
            samesite="lax",
        )

        # Log page view for HTML responses
        content_type = response.headers.get("content-type", "")
        if request.method == "GET" and "text/html" in content_type:
            pv = PageView(
                session_id=session_id,
                page=request.url.path,
                variant_name=variant,
            )
            db.add(pv)
            db.commit()

        db.close()
        return response


app = FastAPI(title=settings.APP_NAME)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Middleware
app.add_middleware(SessionVariantMiddleware)


@app.on_event("startup")
def on_startup():
    init_db()


# Routers
app.include_router(pages.router)
app.include_router(api.router, prefix="/api")
