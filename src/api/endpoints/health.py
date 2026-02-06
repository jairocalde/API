# src/api/endpoints/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.database import get_db

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Endpoint de verificación de salud de la API"""
    return {"status": "healthy", "service": "chat-message-api"}

@router.get("/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Endpoint de verificación de preparación (incluye DB)"""
    try:
        # Verificar que la base de datos responde
        db.execute(text("SELECT 1"))
        return {
            "status": "ready", 
            "service": "chat-message-api",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "service": "chat-message-api", 
            "database": "disconnected",
            "error": str(e)
        }, 503