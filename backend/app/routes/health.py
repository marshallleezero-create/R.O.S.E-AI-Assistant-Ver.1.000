"""
Health check routes
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Check if ROSE is running"""
    return {
        "status": "healthy",
        "service": "ROSE",
        "version": "1.0.0"
    }

@router.get("/status")
async def status():
    """Get detailed status"""
    return {
        "status": "running",
        "components": {
            "api": "ready",
            "database": "ready",
            "llm": "ready",  # TODO: Check if Ollama is accessible
            "agent": "ready"
        }
    }
