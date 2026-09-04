# Getting Started

Get ROSE up and running in 5 minutes.

## Prerequisites

Before installing ROSE, ensure you have:

- **Python 3.11 or higher**
- **pip** (Python package manager)
- **PostgreSQL 12+** (or SQLite for local development)
- **Docker** (optional, for containerized deployment)
- **Node.js** (optional, for dashboard development)

Check your versions:

```bash
python --version       # Should be 3.11+
pip --version          # Any recent version
```

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/rose.git
cd rose
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI – Web framework
- SQLAlchemy – Database ORM
- requests – HTTP client
- And all other dependencies

### Step 3: Run Setup Wizard

The interactive setup wizard configures ROSE for your environment:

```bash
python setup_wizard.py
```

You'll be prompted to configure:
- ✅ Database connection (PostgreSQL or SQLite)
- ✅ LLM provider (local Ollama or cloud API)
- ✅ API credentials (if using cloud LLMs)
- ✅ Autonomy mode (enable self-directed research)
- ✅ Vision & voice modules (Whisper, Piper)

The wizard generates:
- `config.yaml` – Configuration file
- `secrets.env` – API keys (⚠️ Keep safe!)
- `plugins/` – Plugin directory
- `data/` – Data storage

## Running ROSE

### Start the Backend

```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Start the LLM Proxy (in another terminal)

If using a local LLM (Ollama):

```bash
# First, make sure Ollama is running
ollama serve

# In another terminal, start the proxy
uvicorn llm_server:app --port 8001 --reload
```

If using OpenAI/Claude:
- The proxy will use your API key from `secrets.env`
- No local LLM needed

### Open the Dashboard

Visit in your browser:
```
http://localhost:8000/dashboard
```

Or open directly:
```bash
open frontend/dashboard.html
```

## Test Your Installation

### Health Check

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Create a Chat Session

```bash
curl -X POST http://localhost:8000/api/chat/sessions
```

Should return:
```json
{
  "session_id": "sess-abc123",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Send a Message

```bash
curl -X POST http://localhost:8000/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What can you do?",
    "session_id": "sess-abc123"
  }'
```

Should get a response from your LLM!

## Troubleshooting

### "Connection refused" on port 8000

Another process is using port 8000:

```bash
# Find the process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use a different port
uvicorn main:app --port 8001 --reload
```

### "Database connection failed"

Check your PostgreSQL is running:

```bash
# Start PostgreSQL (macOS with Homebrew)
brew services start postgresql

# Or Docker
docker run --name rose-db -e POSTGRES_PASSWORD=password -p 5432:5432 postgres
```

Update `DATABASE_URL` in `config.yaml` or `secrets.env`.

### "LLM not responding"

If using Ollama:

```bash
# Make sure Ollama is running
ollama serve

# Pull a model
ollama pull llama2

# Test it
curl http://localhost:11434/api/tags
```

If using OpenAI/Claude:
- Check your `LLM_API_KEY` in `secrets.env`
- Verify your API key is valid
- Check your account has available credits

### "Module not found" errors

Reinstall dependencies:

```bash
pip install --upgrade -r requirements.txt
```

## Next Steps

Now that ROSE is running:

1. **Explore the Dashboard** – Try the chat, experiment browser, plots
2. **Create an Experiment** – Log your first result
3. **Read the Docs** – Understand the architecture
4. **Build a Tool** – Add custom capabilities
5. **Deploy** – Move to production

### Recommended Reading

- [Setup Wizard Guide](setup-wizard.md) – Deep dive on configuration
- [Architecture Overview](architecture.md) – How ROSE works
- [Tools Guide](tools.md) – Building custom tools
- [Deployment](deployment.md) – Production setup

## System Requirements

### Minimum

- Python 3.11+
- 4 GB RAM
- 1 GB disk space
- PostgreSQL 12+ OR SQLite

### Recommended

- Python 3.11+
- 8+ GB RAM
- 10 GB disk space (for data/models)
- PostgreSQL 15+ (production)
- GPU (for faster inference)

### For Local LLM (Ollama)

- 8+ GB RAM
- GPU recommended (NVIDIA, AMD, or M1/M2 Mac)
- 15+ GB disk (for models)

## Hardware Support

ROSE runs on:
- ✅ Linux (recommended for servers)
- ✅ macOS (including M1/M2)
- ✅ Windows (with WSL2 recommended)
- ✅ Raspberry Pi 4+ (with limitations)
- ✅ Cloud VMs (AWS, GCP, Azure)

## What's Included

✅ Backend API (FastAPI)  
✅ Web Dashboard  
✅ Setup Wizard  
✅ Tool system  
✅ Plugin framework  
✅ LLM integration  
✅ Database ORM  
✅ Documentation  

## What's Optional

🔄 Docker (for containerization)  
🔄 PostgreSQL (SQLite works for dev)  
🔄 GPU (CPU-only is fine)  
🔄 Ollama (if using cloud LLMs)  
🔄 Kubernetes (for scaling)  

---

**Next:** [Setup Wizard](setup-wizard.md) for detailed configuration
