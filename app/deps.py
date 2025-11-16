# app/deps.py
from fastapi.templating import Jinja2Templates
from fastapi import Request, HTTPException
from jinja2 import TemplateNotFound

templates = Jinja2Templates(directory="app/templates")


def common_context(request: Request, title: str | None = None):
    return {
        "request": request,
        "current_variant": getattr(request.state, "variant", None),
        "title": title,
    }


def render_variant_template(
    request: Request,
    template_name: str,
    context: dict,
):
    """
    Renders a template with optional variant-specific override.

    - First tries:  variants/<current_variant>/<template_name>
    - If not found: falls back to template_name

    That lets you create full-page variant templates simply by
    placing them in app/templates/variants/<variant>/.
    """
    from jinja2 import TemplateNotFound  # just in case import above changes

    variant = getattr(request.state, "variant", None)
    ctx = dict(context)  # copy to avoid surprises
    ctx.setdefault("current_variant", variant)

    # Try variant-specific template first
    if variant:
        variant_path = f"variants/{variant}/{template_name}"
        try:
            return templates.TemplateResponse(variant_path, ctx)
        except TemplateNotFound:
            # silently fall back
            pass

    # Fall back to default template
    try:
        return templates.TemplateResponse(template_name, ctx)
    except TemplateNotFound:
        raise HTTPException(status_code=500, detail=f"Template not found: {template_name}")


def jinja_load_variant_template(template_html: str, variant: str | None = None) -> str:
    """
    This function will be used in the HTML files to include variants with jinja.
    How to use it: {% include jinja_load_variant_template("partials/hero.html", current_variant) %}

    Returns the best template path for an include:
    - If variant is set and variants/<variant>/<template_html> exists, return that
    - Otherwise return template_html
    """
    if variant:
        candidate = f"variants/{variant}/{template_html}"
        try:
            templates.env.get_template(candidate)
            return candidate
        except TemplateNotFound:
            # fall back to default
            pass
    return template_html


# register helper as a global in Jinja
templates.env.globals["jinja_load_variant_template"] = jinja_load_variant_template
