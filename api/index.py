"""Vercel ASGI entrypoint.

Vercel's Python runtime discovers this file automatically and serves `app`.
"""

from app.main import app
