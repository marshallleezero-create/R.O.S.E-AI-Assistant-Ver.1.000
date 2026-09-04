"""
ROSE - Research Operations for Scientific Experimentation
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routes import chat, health, experiments
from app.database import init_db

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🌹 ROSE starting up...")
    init_db()
    yield
    # Shutdown
    print("🌹 ROSE shutting down...")

# Create app
app = FastAPI(
    title="ROSE - Research Operations for Scientific Experimentation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, tags=["health"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(experiments.router, prefix="/api/experiments", tags=["experiments"])

@app.get("/")
async def root():
    return {
        "message": "🌹 ROSE is ready for research",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
