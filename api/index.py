"""Vercel ASGI entrypoint.

Vercel serves this file as the Python function. We add `src/` to `sys.path`
so the app package is importable without packaging the whole repository.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from app.main import app
