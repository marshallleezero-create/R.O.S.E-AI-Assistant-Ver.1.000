"""
Database initialization and models
"""
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

# Create engine
engine = create_engine(f"sqlite:///{settings.DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # user, assistant
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    status = Column(String)  # running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    config = Column(JSON)

class ExperimentRun(Base):
    __tablename__ = "experiment_runs"
    
    id = Column(String, primary_key=True, index=True)
    experiment_id = Column(String, index=True)
    parameters = Column(JSON)
    results = Column(JSON)
    metrics = Column(JSON)
    status = Column(String)  # running, completed, failed
    timestamp = Column(DateTime, default=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    message_count = Column(Integer, default=0)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
