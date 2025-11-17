# app/variants.py
from pathlib import Path

TEMPLATES_DIR = Path("app/templates")
VARIANTS_DIR = TEMPLATES_DIR / "variants"


def get_available_variants() -> list[str]:
    if not VARIANTS_DIR.exists():
        return ['default']
    return sorted(
        d.name for d in VARIANTS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    )