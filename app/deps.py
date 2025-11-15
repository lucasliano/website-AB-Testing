from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates")

def common_context(request: Request, title: str | None = None):
    return {
        "request": request,
        "current_variant": getattr(request.state, "variant", "hero_A"),
        "title": title or "RF Analyzer"
    }
