from fastapi import APIRouter, Request
from ..deps import common_context, render_variant_template

router = APIRouter()

@router.get("/")
def home(request: Request):
    ctx = common_context(request, title="RF Analyzer - Home")
    return render_variant_template(request, "home.html", ctx)


@router.get("/product")
def product(request: Request):
    ctx = common_context(request, title="RF Analyzer - Product")
    return render_variant_template(request, "product.html", ctx)


@router.get("/universities")
def universities(request: Request):
    ctx = common_context(request, title="RF Analyzer - Universities")
    return render_variant_template(request, "universities.html", ctx)


@router.get("/documentation")
def documentation(request: Request):
    ctx = common_context(request, title="RF Analyzer - Documentation")
    return render_variant_template(request, "documentation.html", ctx)


@router.get("/about")
def about(request: Request):
    ctx = common_context(request, title="RF Analyzer - About")
    return render_variant_template(request, "about.html", ctx)
