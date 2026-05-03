from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/healthz")
async def health_check():
    return {"ok": True}

@router.get("/metadata")
async def get_metadata():
    return {
        "bot_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "deterministic": True,
        "supported_scopes": settings.SUPPORTED_SCOPES
    }
