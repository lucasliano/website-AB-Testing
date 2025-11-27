import json
import os
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Request, HTTPException
from ..deps import common_context, render_variant_template

router = APIRouter()

def load_initiatives() -> List[Dict[str, Any]]:
    """Temporary in-memory initiatives so the templates have something to render.
    Replace this entirely with your real data access layer.
    """
    filepath = os.path.dirname(os.path.abspath(__file__)) + '/cards.json'
    with open(filepath, "r") as read_file:
        data = json.load(read_file)
    return data
    

def _get_initiative_by_id(initiative_id: int) -> Optional[Dict[str, Any]]:
    for initiative in load_initiatives():
        if initiative["id"] == initiative_id:
            return initiative
    return None

@router.get("/", name="home")
def home(request: Request):
    initiatives = load_initiatives()
    ctx = common_context(request, title="Iniciativas")
    ctx.update({"initiatives": initiatives,})
    return render_variant_template(request, "home.html", ctx)

@router.get("/about", name="about")
def about(request: Request):
    ctx = common_context(request, title="GIAR")
    return render_variant_template(request, "about.html", ctx)

@router.get("/initiatives/{initiative_id}", name="initiative_detail")
def initiative_detail(request: Request, initiative_id: int):
    """Detail page for a single initiative."""
    initiative = _get_initiative_by_id(initiative_id)
    if initiative is None:
        raise HTTPException(status_code=404, detail="Iniciativa no encontrada")

    ctx = common_context(
        request,
        title=f"{initiative['title']} · Iniciativas",
    )
    ctx.update({"initiative": initiative})

    return render_variant_template(request, "initiative_detail.html", ctx)
