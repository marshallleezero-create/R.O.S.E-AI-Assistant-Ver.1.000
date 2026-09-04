# Getting Started with ROSE

## Prerequisites

- Python 3.9+
- pip
- Git
- (Optional) Ollama for local LLM

## Installation

### 1. Clone & Setup
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Start Ollama (Optional)
If using local LLM:
```bash
# Download Ollama from https://ollama.ai
# Run in terminal:
ollama pull llama2
ollama serve
# This starts on http://localhost:11434
```

### 4. Run the Server
```bash
# From backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## API Examples

### Health Check
```bash
curl http://localhost:8000/health
```

### Create Chat Session
```bash
curl -X POST http://localhost:8000/api/chat/sessions
```

### Send Message
```bash
curl -X POST http://localhost:8000/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is ROSE?"}
    ],
    "temperature": 0.7,
    "session_id": "your-session-id"
  }'
```

### Create Experiment
```bash
curl -X POST http://localhost:8000/api/experiments \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Experiment",
    "description": "First test run",
    "config": {"model": "test", "params": {}}
  }'
```

## Project Structure

```
R.O.S.E-AI-Assistant-Ver.1.000/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── config.py         # Settings management
│   │   ├── database.py       # SQLAlchemy models
│   │   ├── services/         # Business logic
│   │   │   ├── llm.py        # LLM integration
│   │   │   └── agent.py      # Agent orchestration
│   │   └── routes/           # API endpoints
│   │       ├── chat.py       # Chat endpoints
│   │       ├── experiments.py # Experiment endpoints
│   │       └── health.py     # Health checks
│   └── requirements.txt      # Python dependencies
├── frontend/                 # (Phase 1+) Web UI
├── docs/
│   ├── ARCHITECTURE.md       # System design
│   └── QUICKSTART.md         # This file
└── config/                   # Configuration files
```

## Configuration Options

### LLM Provider
- `ollama`: Use local Ollama (free, ~8GB RAM)
- `openai`: Use OpenAI API (paid, better quality)
- `claude`: Use Claude API (paid, strong reasoning)

### Models
- **Ollama**: llama2, mistral, neural-chat, etc.
- **OpenAI**: gpt-4, gpt-3.5-turbo
- **Claude**: claude-3-opus, claude-3-sonnet

### Whisper Models (Phase 2)
- `tiny`: Fastest, lower accuracy
- `base`: Good balance (recommended)
- `small`, `medium`, `large`: Better but slower

## Troubleshooting

### "Connection refused" on Ollama
- Make sure Ollama is running: `ollama serve`
- Check OLLAMA_BASE_URL in .env

### LLM responses are slow
- Using local model? It depends on your hardware
- Consider cloud fallback in .env

### Database errors
- Delete `data/rose.db` to reset
- Ensure `data/` directory exists

## Next Steps

- **Phase 1 completion**: Build frontend (React/Vue)
- **Phase 2**: Add voice input/output (Whisper + Piper)
- **Phase 3**: Vision support (LLaVA)
- **Phase 4**: ML pipelines and experiment automation

## Documentation

- [Architecture](./ARCHITECTURE.md) - System design & components
- [API Reference](./API.md) - Endpoint documentation (coming soon)
- [Tool Development](./TOOLS.md) - Creating custom tools (coming soon)
