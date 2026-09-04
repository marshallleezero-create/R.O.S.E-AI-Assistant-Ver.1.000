"""
ROSE configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # LLM
    LLM_PROVIDER: str = "ollama"  # ollama, openai, claude, gemini
    LLM_MODEL: str = "llama2"
    LLM_API_KEY: str = ""
    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Cloud API Keys
    OPENAI_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""
    
    # Storage
    DB_PATH: str = "./data/rose.db"
    DATA_DIR: str = "./data"
    EXPERIMENTS_DIR: str = "./experiments"
    
    # Speech & Vision
    WHISPER_MODEL: str = "base"
    TTS_ENGINE: str = "piper"
    VISION_MODEL: str = "local"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/rose.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Ensure directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.EXPERIMENTS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
