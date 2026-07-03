"""
Health check endpoints.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "repopilot-api",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check - verifies dependencies are available."""
    # TODO: Add actual dependency checks (database, redis, chromadb)
    return {
        "status": "ready",
        "checks": {
            "database": "ok",
            "redis": "ok",
            "chromadb": "ok"
        }
    }


@router.get("/live")
async def liveness_check():
    """Liveness check - confirms service is running."""
    return {"status": "alive"}
