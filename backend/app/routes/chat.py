"""
Chat API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import get_db, ChatSession as ChatSessionModel, Message as MessageModel
from app.services.llm import llm_service
from app.services.agent import agent_service

router = APIRouter()

class MessageSchema(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[MessageSchema]
    temperature: float = 0.7
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    timestamp: datetime

@router.post("/completions")
async def chat_completion(request: ChatRequest, db: Session = Depends(get_db)):
    """Send messages to ROSE and get completion"""
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        
        # Convert to LLM format
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        # Get response from LLM
        response_text = await llm_service.chat(messages, request.temperature)
        
        # Store in database
        message_id = str(uuid.uuid4())
        db_message = MessageModel(
            id=message_id,
            session_id=session_id,
            role="assistant",
            content=response_text,
            timestamp=datetime.utcnow()
        )
        db.add(db_message)
        db.commit()
        
        return ChatResponse(
            id=message_id,
            session_id=session_id,
            role="assistant",
            content=response_text,
            timestamp=db_message.timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions")
async def create_session(db: Session = Depends(get_db)):
    """Create new chat session"""
    session_id = str(uuid.uuid4())
    db_session = ChatSessionModel(
        id=session_id,
        title=f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        created_at=datetime.utcnow()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return {
        "id": db_session.id,
        "title": db_session.title,
        "created_at": db_session.created_at
    }

@router.get("/sessions/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    """Get chat session details"""
    session = db.query(ChatSessionModel).filter(ChatSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = db.query(MessageModel).filter(MessageModel.session_id == session_id).all()
    
    return {
        "id": session.id,
        "title": session.title,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "message_count": len(messages),
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp
            }
            for m in messages
        ]
    }

@router.post("/research")
async def research_query(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Specialized research mode: ROSE plans and executes research steps
    Phase 2+ feature with tool integration
    """
    session_id = request.session_id or str(uuid.uuid4())
    
    # Extract goal from last user message
    goal = request.messages[-1].content if request.messages else "Conduct research"
    
    # Create agent and run task
    agent_id = str(uuid.uuid4())
    result = await agent_service.run_task(agent_id, goal, {"session_id": session_id})
    
    return {
        "session_id": session_id,
        "agent_id": agent_id,
        "goal": goal,
        "execution": result
    }
