# 🌹 ROSE Quick Reference

## Getting Started in 30 Seconds

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
python setup_wizard.py

# 3. Run
uvicorn main:app --reload

# 4. Open
# http://localhost:8000
```

---

## Key Commands

```bash
# Development
python setup_wizard.py           # Interactive configuration
uvicorn main:app --reload       # Start backend (port 8000)
uvicorn llm_server:app --port 8001 --reload  # Start LLM proxy

# Ollama (local LLM)
ollama serve                     # Start Ollama
ollama pull llama2               # Download model

# Documentation
mkdocs serve                     # View docs locally
mkdocs build                     # Build static site

# Testing
pytest tests/                    # Run tests
python -m pytest --cov          # With coverage
```

---

## API Endpoints (REST)

```bash
# Chat
POST   /api/chat/completions     Send message
GET    /api/chat/sessions        List sessions
POST   /api/chat/sessions        Create session
GET    /api/chat/sessions/{id}   Get history

# Tools
GET    /tools                    List tools
POST   /tools/{name}             Execute tool

# Experiments
POST   /api/experiments          Create experiment
GET    /api/experiments/{id}     Get experiment
PATCH  /api/experiments/{id}     Update results

# Autonomy
POST   /autonomy/run             Start autonomous workflow
GET    /autonomy/run/{id}        Get status
```

---

## Configuration

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/rose

# LLM
LLM_PROVIDER=ollama              # or openai, claude
LLM_API_KEY=sk-...
OLLAMA_BASE_URL=http://localhost:11434

# Vision & Voice
VISION_API_KEY=sk-...
WHISPER_CMD=whisper
PIPER_CMD=piper

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

---

## Directory Structure

```
rose/
├── backend/                 # API server code
│   ├── main.py             # FastAPI app
│   ├── llm_server.py       # LLM proxy
│   └── tools/              # Tools registry
├── frontend/               # Web dashboard
├── plugins/                # Plugin directory
├── data/                   # Data storage
├── docs/                   # Documentation
├── tests/                  # Test suite
├── config.yaml             # Configuration
├── secrets.env            # API keys (⚠️ secret)
└── setup_wizard.py        # Setup tool
```

---

## Project Links

| Resource | URL |
|----------|-----|
| Main Repo | `https://github.com/your-org/rose` |
| Issues | `/issues` |
| Discussions | `/discussions` |
| Docs Site | `http://docs.rose.local` |
| Dashboard | `http://localhost:8000` |

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `lsof -i :8000` then kill process |
| DB connection fails | Verify PostgreSQL running or use SQLite |
| LLM not responding | Check Ollama: `ollama serve` |
| Module not found | `pip install --upgrade -r requirements.txt` |
| API key error | Check `secrets.env` has correct key |

---

## File Locations

| File | Purpose |
|------|---------|
| README.md | Main documentation |
| mkdocs.yml | MkDocs configuration |
| docs/index.md | Docs homepage |
| docs/getting-started.md | Installation guide |
| docs/architecture.md | System design |
| setup_wizard.py | Configuration wizard |
| config.yaml | Main config |
| secrets.env | API keys (secret) |

---

## Helpful Commands

```bash
# Check Python version
python --version              # Need 3.11+

# Create virtual env
python -m venv venv
source venv/bin/activate      # Or venv\Scripts\activate on Windows

# Install deps
pip install -r requirements.txt

# Format code
black .

# Lint code
flake8 .

# Type check
mypy .

# Build docs
mkdocs build

# Test docs locally
mkdocs serve

# Deploy docs
# Push site/ to GitHub Pages, Netlify, etc.
```

---

## Integration Examples

### Chat with ROSE

```bash
curl -X POST http://localhost:8000/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What can you do?",
    "session_id": "sess-123"
  }'
```

### Run a Tool

```bash
curl -X POST http://localhost:8000/tools/run_simulation \
  -H "Content-Type: application/json" \
  -d '{
    "model": "simulation.py",
    "param": 0.5,
    "iterations": 100
  }'
```

### Start Autonomous Research

```bash
curl -X POST http://localhost:8000/autonomy/run \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Optimize reaction rate",
    "constraints": {"no_network": true},
    "human_approval": true
  }'
```

---

## Resources

- 📖 Full Docs: Read `README.md` first
- 🚀 Getting Started: See `docs/getting-started.md`
- 🏗️ Architecture: Check `docs/architecture.md`
- 🛠️ Tools: Learn `docs/tools.md`
- ⚙️ Configuration: Use `setup_wizard.py`

---

## Support

- 💬 Questions? Check docs or GitHub discussions
- 🐛 Found a bug? Open GitHub issue
- 💡 Have an idea? Create discussion
- 📧 Contact: [support@rose.local]

---

**Last Updated:** 2026-09-04  
**Version:** 1.0.0  
**Status:** ✅ Ready to use
