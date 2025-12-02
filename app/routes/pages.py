from fastapi import APIRouter, Request, HTTPException
from ..deps import common_context, render_variant_template

router = APIRouter()

@router.get("/", name="home")
def home(request: Request):
    ctx = common_context(request, title="LaserMakers")
    return render_variant_template(request, "home.html", ctx)