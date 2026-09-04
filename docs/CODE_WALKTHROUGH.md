# ROSE Code Walkthrough

## Overview
This guide explains the key components of ROSE's codebase and how they work together.

## Core Application Flow

```
User Request (HTTP/WebSocket)
       │
       ▼
FastAPI Router (routes/chat.py, routes/experiments.py)
       │
       ├─→ Validate Request (Pydantic models)
       │
       ├─→ Database Session (get_db dependency)
       │
       ├─→ Business Logic
       │   ├─ LLM Service: llm.chat(), llm.stream_chat()
       │   ├─ Agent Service: agent.plan(), agent.execute()
       │   └─ Database: Store/retrieve messages, experiments
       │
       ▼
Response (JSON or Stream)
```

## Main Components

### 1. FastAPI Application (`app/main.py`)

```python
# The root of everything
app = FastAPI()  # Creates HTTP server

# Lifecycle management
@asynccontextmanager
async def lifespan(app):
    init_db()  # On startup
    yield
    # shutdown cleanup

# CORS middleware for frontend
app.add_middleware(CORSMiddleware, ...)

# Include routers
app.include_router(chat.router)      # /api/chat/*
app.include_router(experiments.router)  # /api/experiments/*
app.include_router(health.router)    # /health, /status
```

### 2. Configuration (`app/config.py`)

```python
class Settings(BaseSettings):
    # Reads from .env automatically
    LLM_PROVIDER = "ollama"     # or "openai"
    LLM_MODEL = "llama2"
    OLLAMA_BASE_URL = "http://localhost:11434"
    DB_PATH = "./data/rose.db"
    # ... 20+ more settings

settings = Settings()  # Singleton
```

**Usage**: Import `settings` anywhere in the code to access configuration.

### 3. Database (`app/database.py`)

```python
# SQLAlchemy setup
engine = create_engine(f"sqlite:///{settings.DB_PATH}")
SessionLocal = sessionmaker(bind=engine)

# Models (ORM classes)
class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id: str
    title: str
    created_at: datetime

class Message(Base):
    __tablename__ = "messages"
    id: str
    session_id: str (FK)
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime

# Dependency injection
def get_db():
    db = SessionLocal()
    yield db
    db.close()

# Usage in routes
@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # db is automatically provided by FastAPI
```

### 4. LLM Service (`app/services/llm.py`)

**Purpose**: Unified interface for different LLM providers.

```python
class LLMService:
    async def chat(messages, temperature):
        # Routes to appropriate provider
        if provider == "ollama":
            return await self._ollama_chat(messages, temperature)
        elif provider == "openai":
            return await self._openai_chat(messages, temperature)
    
    async def _ollama_chat(messages, temperature):
        # Call local Ollama server
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/chat",
                json={"model": "llama2", "messages": messages}
            )
        return response.json()["message"]["content"]
    
    async def analyze_text(text, task):
        # Specialized text analysis
        prompt = f"Please {task} the following...\n\n{text}"
        return await self.chat([{"role": "user", "content": prompt}])
```

**Usage**:
```python
from app.services.llm import llm_service

# Anywhere in the app
response = await llm_service.chat(
    [{"role": "user", "content": "What is ROSE?"}],
    temperature=0.7
)
```

### 5. Agent Service (`app/services/agent.py`)

**Purpose**: Orchestrate multi-step reasoning and tool execution.

```python
class Agent:
    state: AgentState  # THINKING → PLANNING → EXECUTING → REFLECTING → DONE
    steps: List[AgentStep]  # Individual actions
    
    async def plan(goal: str):
        # Break goal into steps (currently simple, will use LangChain)
        steps = [
            AgentStep("understand", "Understand the goal"),
            AgentStep("research", "Search for information"),
            AgentStep("analyze", "Analyze findings"),
            AgentStep("synthesize", "Combine results"),
        ]
        return steps
    
    async def execute():
        # Run each step
        for step in self.steps:
            step.status = "running"
            step.result = await self._execute_action(step.action)
            step.status = "done"

class AgentService:
    agents: Dict[str, Agent]  # Manage multiple agents
    
    async def run_task(agent_id, goal, context):
        # Create, plan, and execute
        agent = Agent()
        await agent.plan(goal, context)
        return await agent.execute()
```

**Usage** (Phase 2 Research Mode):
```python
# User asks: "Run a parameter sweep on my simulation"
result = await agent_service.run_task(
    agent_id="exp-123",
    goal="Run a parameter sweep on my simulation",
    context={"experiment_id": "exp-456"}
)
# Agent plans: load config → run sims → analyze → report
# Then executes each step
```

### 6. Chat Routes (`app/routes/chat.py`)

```python
@router.post("/api/chat/completions")
async def chat_completion(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Validate request
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    
    # 2. Call LLM
    response_text = await llm_service.chat(messages, request.temperature)
    
    # 3. Store in database
    db_message = Message(
        id=uuid.uuid4(),
        session_id=request.session_id,
        role="assistant",
        content=response_text
    )
    db.add(db_message)
    db.commit()
    
    # 4. Return response
    return ChatResponse(
        id=db_message.id,
        session_id=request.session_id,
        role="assistant",
        content=response_text,
        timestamp=db_message.timestamp
    )

@router.post("/api/chat/research")
async def research_query(request: ChatRequest, db: Session = Depends(get_db)):
    # Research mode: plan + execute
    goal = request.messages[-1].content
    agent_id = uuid.uuid4()
    
    result = await agent_service.run_task(
        agent_id,
        goal,
        {"session_id": request.session_id}
    )
    
    return {
        "agent_id": agent_id,
        "goal": goal,
        "execution": result  # Steps, results, final synthesis
    }
```

### 7. Experiment Routes (`app/routes/experiments.py`)

```python
@router.post("/api/experiments")
async def create_experiment(exp: ExperimentSchema, db: Session = Depends(get_db)):
    db_exp = Experiment(
        id=uuid.uuid4(),
        name=exp.name,
        description=exp.description,
        config=exp.config,  # Stored as JSON
        status="created"
    )
    db.add(db_exp)
    db.commit()
    return db_exp

@router.post("/api/experiments/{id}/runs")
async def create_run(experiment_id, run: ExperimentRunSchema, db: Session = Depends(get_db)):
    # Create a run for an experiment (parameter combination)
    db_run = ExperimentRun(
        id=uuid.uuid4(),
        experiment_id=experiment_id,
        parameters=run.parameters,  # {"learning_rate": 0.01, ...}
        status="created"
    )
    db.add(db_run)
    db.commit()

@router.patch("/api/experiments/{id}/runs/{run_id}")
async def update_run(experiment_id, run_id, data, db: Session = Depends(get_db)):
    # Update with results after execution
    run = db.query(ExperimentRun).filter_by(id=run_id).first()
    run.results = data["results"]     # {"accuracy": 0.95, ...}
    run.metrics = data["metrics"]     # {"loss": 0.05, ...}
    run.status = "completed"
    db.commit()
```

## Request/Response Flow Example

### Chat Request
```
POST /api/chat/completions
{
  "messages": [
    {"role": "user", "content": "Summarize machine learning"}
  ],
  "temperature": 0.7,
  "session_id": "sess-123"
}

↓ (FastAPI Pydantic validation)

↓ (Get database session from Depends(get_db))

↓ (Call LLM Service)
llm_service.chat([{"role": "user", "content": "..."}])
  → httpx call to Ollama/OpenAI
  → receive response

↓ (Store in database)
Message(
  id="msg-456",
  session_id="sess-123",
  role="assistant",
  content="Machine learning is...",
  timestamp=now
)
db.add(message)
db.commit()

↓ Response:
{
  "id": "msg-456",
  "session_id": "sess-123",
  "role": "assistant",
  "content": "Machine learning is...",
  "timestamp": "2026-08-31T12:49:45"
}
```

## Key Design Patterns

### 1. Dependency Injection
```python
# FastAPI automatically provides dependencies
async def route_handler(
    request: RequestModel,
    db: Session = Depends(get_db),  # Database session
    service: LLMService = Depends(get_llm_service)  # Service instance
):
    pass
```

### 2. Async/Await
```python
# All I/O is async for performance
async def chat(messages):
    # No blocking—other requests can be handled
    response = await llm_service.chat(messages)
    return response
```

### 3. Pydantic Models
```python
# Automatic validation + serialization
class ChatRequest(BaseModel):
    messages: List[MessageSchema]
    temperature: float = 0.7

# FastAPI validates incoming JSON against this schema
@router.post()
async def route(request: ChatRequest):
    # request.messages is guaranteed to be correct type
```

### 4. Service Layer
```python
# Separates API (routes) from logic (services)
# Easy to test, reuse, swap implementations
app/routes/chat.py      # What the API looks like
app/services/llm.py     # How it works
```

## Adding New Features

### Add a New API Endpoint

1. **Define Pydantic model** in routes file:
```python
class NewFeatureRequest(BaseModel):
    input_data: str
```

2. **Implement route**:
```python
@router.post("/api/feature")
async def new_feature(req: NewFeatureRequest, db: Session = Depends(get_db)):
    # Business logic here
    return {"result": "..."}
```

3. **Add database model** if needed in `database.py`:
```python
class NewFeatureLog(Base):
    __tablename__ = "feature_logs"
    id = Column(String, primary_key=True)
    # ...
```

### Integrate New LLM Provider

1. **Add method to `LLMService`**:
```python
async def _claude_chat(self, messages, temperature):
    # Call Claude API
```

2. **Update `chat()` method**:
```python
elif self.provider == "claude":
    return await self._claude_chat(messages, temperature)
```

3. **Add config in `.env.example`**:
```env
LLM_PROVIDER=claude
CLAUDE_API_KEY=sk-ant-...
```

## Testing

```python
# Basic test in tests/test_api.py
def test_chat_completion():
    response = client.post("/api/chat/completions", json={
        "messages": [{"role": "user", "content": "Hi"}]
    })
    assert response.status_code == 200
    assert response.json()["role"] == "assistant"
```

Run tests:
```bash
pytest backend/tests/ -v
```

## Performance Considerations

1. **Database**: Add indexes for frequently queried columns
2. **LLM**: Streaming responses for long outputs (use `stream_chat()`)
3. **Caching**: Session caching with Redis (Phase 2+)
4. **Pagination**: Limit returned messages/experiments
5. **Async**: All I/O is async—always use `await`

---

**Next**: Look at `docs/QUICKSTART.md` to get the server running!
