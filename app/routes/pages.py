import json
import os
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from starlette import status
from ..deps import common_context, render_variant_template

router = APIRouter()

# @router.get("/")
# def home(request: Request):
#     ctx = common_context(request, title="RF Analyzer - Home")
#     return render_variant_template(request, "home.html", ctx)


# @router.get("/product")
# def product(request: Request):
#     ctx = common_context(request, title="RF Analyzer - Product")
#     return render_variant_template(request, "product.html", ctx)


# @router.get("/universities")
# def universities(request: Request):
#     ctx = common_context(request, title="RF Analyzer - Universities")
#     return render_variant_template(request, "universities.html", ctx)


# @router.get("/documentation")
# def documentation(request: Request):
#     ctx = common_context(request, title="RF Analyzer - Documentation")
#     return render_variant_template(request, "documentation.html", ctx)


# @router.get("/about")
# def about(request: Request):
#     ctx = common_context(request, title="RF Analyzer - About")
#     return render_variant_template(request, "about.html", ctx)


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
    ctx = common_context(request, title="Iniciativas - Home")
    ctx.update({"initiatives": initiatives,})
    return render_variant_template(request, "home.html", ctx)


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


@router.post("/initiatives/submit", name="submit_initiative")
def submit_initiative(
    request: Request,
    title: str = Form(...),
    owner: str = Form(...),
    email: str = Form(...),
    status_value: str = Form(..., alias="status"),
    summary: str = Form(...),
    description: str = Form(""),
    categories: str = Form(""),  # comma-separated from the pill group
    needs: str = Form(""),  # single value from the pill group
):
    """Handle the 'Postulá tu iniciativa' form from the modal.

    Right now this is just a stub - you should:
      - validate the payload
      - persist it (DB, spreadsheet, etc.)
      - maybe send notification emails
    """
    # TODO: Replace with your persistence layer
    # Example payload you might want to pass to a service layer:
    payload = {
        "title": title,
        "owner": owner,
        "email": email,
        "status": status_value,
        "summary": summary,
        "description": description,
        "categories": [c.strip() for c in categories.split(",") if c.strip()],
        "needs": needs,
    }
    # For now we just log / debug-print; a real app would save this.
    print(payload)  # noqa: T201 (if you use flake8-print or similar)

    # After handling the submission, redirect back to the home page
    url = request.app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)