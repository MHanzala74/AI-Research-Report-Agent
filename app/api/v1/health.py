"""Health check endpoint."""
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "version": settings.app_version, "environment": settings.app_env}
