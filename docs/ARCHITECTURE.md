# ROSE Architecture

## Overview
ROSE (Research Operations for Scientific Experimentation) is a modular AI assistant designed for research workflows. It combines:
- **Multimodal AI**: Text, speech, images, video understanding
- **Agentic reasoning**: Planning, tool use, reflection
- **Experiment tracking**: Data logging, reproducibility
- **Cost efficiency**: Hybrid local + cloud models

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│  User Interface (Web/Mobile/Voice)                  │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│  FastAPI Backend (Port 8000)                        │
├──────────────────────────────────────────────────────┤
│  Routes:                                            │
│  • /api/chat/completions     - Text completions     │
│  • /api/chat/research         - Research mode       │
│  • /api/experiments           - Experiment mgmt     │
│  • /health                    - Health checks       │
└─────────────────┬───────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┬──────────────────┐
    │             │             │                  │
    ▼             ▼             ▼                  ▼
┌────────┐   ┌────────┐   ┌──────────┐      ┌──────────┐
│ LLM    │   │ Agent  │   │ Database │      │  Tools   │
│Service │   │Service │   │ (SQLite) │      │  Layer   │
└────────┘   └────────┘   └──────────┘      └──────────┘
    │             │             │                  │
 Local:        Plan +      Messages,           Scripts
 Ollama        Execute     Sessions,            APIs
 Remote:       Steps       Experiments         WebSearch
 OpenAI        Tools                          Automation
```

## Components

### 1. FastAPI Backend
- **Port**: 8000
- **Files**: `backend/app/main.py`, `backend/app/config.py`
- Serves REST API for ROSE interactions
- Handles sessions, messaging, and experiment management

### 2. LLM Service (`backend/app/services/llm.py`)
- Unified interface for local and cloud models
- Providers: Ollama (local), OpenAI (cloud)
- Methods: `chat()`, `stream_chat()`, `analyze_text()`, `generate_hypothesis()`

### 3. Agent Service (`backend/app/services/agent.py`)
- Orchestrates multi-step reasoning
- States: THINKING → PLANNING → EXECUTING → REFLECTING → DONE
- Implements planning and tool execution loop
- TODO: Integrate LangChain/AutoGen for advanced orchestration

### 4. Database (`backend/app/database.py`)
- SQLite-based storage
- Tables:
  - `chat_sessions`: Conversation tracking
  - `messages`: Chat history
  - `experiments`: Experiment definitions
  - `experiment_runs`: Individual runs with parameters/results

### 5. API Routes
- **Chat** (`backend/app/routes/chat.py`):
  - POST `/api/chat/completions` - Send messages to ROSE
  - POST `/api/chat/research` - Research mode with agent
  - POST `/api/chat/sessions` - Create session
  - GET `/api/chat/sessions/{session_id}` - Get session details

- **Experiments** (`backend/app/routes/experiments.py`):
  - POST `/api/experiments` - Create experiment
  - GET `/api/experiments/{id}` - Get experiment
  - POST `/api/experiments/{id}/runs` - Create run
  - PATCH `/api/experiments/{id}/runs/{run_id}` - Update results

- **Health** (`backend/app/routes/health.py`):
  - GET `/health` - Health check
  - GET `/status` - Component status

## Hardware Compatibility (Intel i5-12450H)

Your machine can run:
- ✅ Local LLM (Llama 2/3, DeepSeek via Ollama)
- ✅ Speech-to-text (Whisper)
- ✅ Text-to-speech (Piper/Kokoro)
- ✅ Vision (LLaVA - slower but functional)
- ✅ Scripting & automation
- ⚠️ Complex ML models (may need GPU optimization)
- 🔄 Cloud fallback for heavy workloads

## Phase Roadmap

### Phase 1: Text Brain ✓ (Current)
- ✅ FastAPI backend
- ✅ LLM integration (Ollama/OpenAI)
- ✅ Basic chat API
- ⏳ Frontend (React/Vue)

### Phase 2: Voice + Tools
- STT (Whisper)
- TTS (Piper)
- Tool system (web search, file ops, calendar)
- Agent framework (LangChain)

### Phase 3: Vision + Analysis
- Image input
- Vision model (LLaVA/cloud)
- Data analysis tools
- Chart generation

### Phase 4: ML + Automation
- Predictive models
- Experiment planning
- Guardrails & confidence scores
- Result logging

## Quick Start

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Set up Ollama (for local LLM)
# Download from https://ollama.ai
# ollama pull llama2

# 3. Copy environment file
cp ../.env.example .env

# 4. Start the server
python -m uvicorn app.main:app --reload --port 8000
```

## Configuration

See `.env.example` for all available settings:
- `LLM_PROVIDER`: ollama, openai, claude
- `LLM_MODEL`: Model name (llama2, gpt-4, etc.)
- `OLLAMA_BASE_URL`: Local Ollama endpoint
- `API_PORT`: Server port (default 8000)

## Next Steps

1. **Frontend**: Build web UI (React/Vue) to interact with API
2. **Tool integration**: Implement web search, file operations
3. **Agent framework**: Integrate LangChain for advanced reasoning
4. **Testing**: Add unit and integration tests
5. **Deployment**: Docker setup, cloud deployment guide
