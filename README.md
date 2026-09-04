# 🌹 ROSE – Research Operations for Scientific Experimentation

**Version 1.0.0** | A modular, multimodal scientific operating system for autonomous research.

## What is ROSE?

ROSE is a programmable AI lab partner designed for:

- **Running simulations** – Execute complex experiments with parameter sweeps
- **Analyzing data** – Statistical analysis, hypothesis generation, predictions
- **Interpreting images** – Vision-based analysis and visualization
- **Autonomous workflows** – Self-directed experiment planning and execution
- **Experiment logging** – Reproducible research with full audit trails
- **Plugin extensibility** – Custom tools, workflows, and integrations
- **Cloud deployment** – Kubernetes-ready, scalable infrastructure

Built for scientists, engineers, and creators who want a programmable research assistant.

---

## 🚀 Quick Start

### Installation

```bash
# Prerequisites: Python 3.11+, PostgreSQL, Docker (optional)

# 1. Clone and install
git clone <repo-url>
cd R.O.S.E-AI-Assistant-Ver.1.000
pip install -r requirements.txt

# 2. Run setup wizard (interactive configuration)
python setup_wizard.py

# 3. Start the backend
uvicorn main:app --reload

# 4. Start the LLM proxy
uvicorn llm_server:app --port 8001 --reload

# 5. Open the dashboard
# Open frontend/dashboard.html in your browser
```

**That's it!** ROSE is running at `http://localhost:8000`

---

## 📋 Table of Contents

- [Getting Started](#quick-start)
- [Setup Wizard](#-setup-wizard)
- [Architecture](#-architecture)
- [Tools & Capabilities](#-tools)
- [Plugin System](#-plugin-system)
- [Autonomous Mode](#-autonomous-mode)
- [Database](#-database)
- [Dashboard](#-dashboard)
- [Deployment](#-deployment)
- [API Reference](#-api-reference)

---

## 🧙 Setup Wizard

ROSE includes an interactive CLI setup wizard that configures:

- **Database connection** – PostgreSQL or SQLite
- **LLM provider** – Local or cloud (OpenAI, Claude, etc.)
- **Autonomy mode** – Enable self-directed research workflows
- **Vision + Voice** – Whisper (STT), Piper (TTS), vision models
- **Plugin system** – Custom tools and extensions
- **Directory structure** – Organized project layout

Run the wizard:

```bash
python setup_wizard.py
```

The wizard generates:
- `config.yaml` – Main configuration
- `secrets.env` – API keys and credentials
- `plugins/` – Plugin directory
- `data/` – Experiment data storage

---

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────┐
│     Multimodal Dashboard (Web UI)       │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         FastAPI Backend (Port 8000)     │
├─────────────────────────────────────────┤
│  • Tool Registry        • Plugin Manager│
│  • API Endpoints        • Autonomy Loop │
│  • Database ORM         • Logging       │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌──────────┐
│LLM     │  │Tool    │  │Database  │
│Proxy   │  │Registry│  │(Postgres)│
└────────┘  └────────┘  └──────────┘
    │            │
    └────────────┼────────────┐
                 │            │
             Local/Cloud   Scientific
             LLMs          Experiment
                          Logging
```

### Key Features

| Component | Purpose |
|-----------|---------|
| **FastAPI Backend** | REST API, tool orchestration, autonomous planning |
| **LLM Proxy** | Unified interface to local/cloud language models |
| **Tool Registry** | Modular, extensible capability system |
| **Plugin Manager** | Safe, sandboxed third-party extensions |
| **Autonomy Orchestrator** | Self-directed research workflow planning |
| **Scientific DB** | PostgreSQL + SQLAlchemy for experiment logging |
| **Multimodal Dashboard** | Chat, simulation runner, plot viewer, voice I/O |

---

## 🛠️ Tools

ROSE includes these built-in tools:

| Tool | Purpose |
|------|---------|
| `run_simulation` | Execute simulations with parameter sweeps |
| `analyze_image` | Vision-based analysis and interpretation |
| `describe_dataset` | Statistical summaries and exploration |
| `linear_regression` | Predictive modeling |
| `generate_hypotheses` | LLM-driven hypothesis generation |
| `log_experiment` | Store results with full metadata |
| `read_file` | File I/O for data loading |
| `web_search` | Internet information retrieval |

Tools are registered in `tools/__init__.py` and can be extended via plugins.

---

## 🔌 Plugin System

ROSE supports a full plugin ecosystem for custom capabilities.

### Create a Plugin

```bash
python plugin_gen.py MyPlugin
```

This generates:
```
plugins/my_plugin/
├── plugin.json          # Metadata
├── plugin.py            # Implementation
└── requirements.txt     # Dependencies
```

### Plugin Features

- **Custom tools** – Add new capabilities
- **Custom workflows** – Chained tool execution
- **Marketplace entries** – Share plugins
- **Sandboxed execution** – Safe third-party code
- **Optional signing** – Verified plugins

### Example Plugin

```python
# plugins/my_plugin/plugin.py
from rose.plugin import RosePlugin, tool

class MyPlugin(RosePlugin):
    name = "My Plugin"
    version = "1.0.0"
    
    @tool
    def my_tool(self, input_data: str) -> str:
        """A custom tool"""
        return f"Processed: {input_data}"
```

---

## 🤖 Autonomous Mode

ROSE can autonomously:

1. **Plan experiments** – Decompose research goals into steps
2. **Execute simulations** – Run parameter sweeps automatically
3. **Analyze results** – Evaluate outcomes and extract insights
4. **Log experiments** – Record all data, parameters, and results
5. **Iterate** – Refine hypotheses until convergence

### Start a Run

```bash
POST /autonomy/run
{
  "goal": "Optimize reaction rate",
  "constraints": {"no_network": true},
  "human_approval": true
}
```

### Autonomy Loop

```
1. Plan (LLM) → Decompose goal into experiment steps
2. Execute → Run simulations/analyses in sequence
3. Analyze → Extract metrics and insights
4. Verify → Check convergence, plan next iteration
5. Log → Store all data with audit trail
6. Repeat until goal achieved or max iterations
```

---

## 💾 Database

ROSE uses PostgreSQL with SQLAlchemy ORM.

### Experiment Schema

```python
class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    goal = Column(String)
    parameters = Column(JSON)        # Input params
    results = Column(JSON)           # Output results
    metrics = Column(JSON)           # Computed metrics
    notes = Column(String)           # Research notes
    status = Column(String)          # running/completed/failed
    timestamp = Column(DateTime)     # Creation time
    updated_at = Column(DateTime)    # Last update
```

### Querying

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(DATABASE_URL)
with Session(engine) as session:
    experiments = session.query(Experiment).all()
    for exp in experiments:
        print(f"{exp.name}: {exp.status}")
```

---

## 📊 Dashboard

The web-based dashboard provides:

| Feature | Purpose |
|---------|---------|
| **Chat** | Conversational research interface |
| **Experiment Browser** | View/manage all logged experiments |
| **Simulation Runner** | Execute simulations with live progress |
| **Plot Viewer** | Visualize results (2D/3D plots) |
| **Image Analysis** | Upload and analyze images |
| **Voice Input** | Hands-free research |
| **Autonomy Controls** | Start/stop autonomous runs |

Open:
```bash
# In browser
frontend/dashboard.html

# Or run dev server
cd frontend
npm install
npm start
```

---

## 🚢 Deployment

### Docker

```bash
docker-compose up --build
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  rose-backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:pass@db/rose
      LLM_API_KEY: ${LLM_API_KEY}
    depends_on:
      - db
      - llm-proxy

  llm-proxy:
    image: llm-proxy:latest
    ports:
      - "8001:8001"

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: rose
      POSTGRES_PASSWORD: rose
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Kubernetes

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployment-rose.yaml
kubectl apply -f kubernetes/deployment-llm.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/configmap.yaml
```

---

## 📡 API Reference

### Chat API

```bash
# Send a message
POST /api/chat/completions
{
  "message": "Analyze this dataset",
  "session_id": "sess-123"
}

# Get session history
GET /api/chat/sessions/{session_id}

# Create new session
POST /api/chat/sessions
```

### Tool API

```bash
# List available tools
GET /tools

# Execute a tool
POST /tools/{tool_name}
{
  "params": {...}
}

# Get tool schema
GET /tools/{tool_name}/schema
```

### Experiment API

```bash
# Create experiment
POST /api/experiments
{
  "name": "Test Run",
  "goal": "Optimize X",
  "parameters": {...}
}

# Get experiment
GET /api/experiments/{id}

# Log results
PATCH /api/experiments/{id}
{
  "results": {...},
  "metrics": {...},
  "status": "completed"
}
```

### Autonomy API

```bash
# Start autonomous run
POST /autonomy/run
{
  "goal": "Optimize reaction rate",
  "constraints": {...},
  "human_approval": true
}

# Get run status
GET /autonomy/run/{run_id}

# List all runs
GET /autonomy/runs
```

---

## 🔧 Configuration

### .env Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/rose

# LLM
LLM_API_URL=http://localhost:8001/llm
LLM_API_KEY=your-key

# Vision & Voice
VISION_API_URL=https://api.openai.com/v1/vision
VISION_API_KEY=your-key
WHISPER_CMD=whisper
PIPER_CMD=piper

# Autonomy
AUTONOMY_ENABLED=true
AUTONOMY_MAX_ITERATIONS=10
HUMAN_APPROVAL_REQUIRED=true

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

---

## 📚 Documentation

Full developer documentation available in the `docs/` folder:

- **[Getting Started](docs/getting-started.md)** – Installation & first steps
- **[Setup Wizard](docs/setup-wizard.md)** – Interactive configuration
- **[Architecture](docs/architecture.md)** – System design
- **[Tools](docs/tools.md)** – Tool system guide
- **[Plugins](docs/plugins.md)** – Plugin development
- **[Autonomy](docs/autonomy.md)** – Autonomous mode details
- **[Database](docs/database.md)** – Database schema & queries
- **[Dashboard](docs/dashboard.md)** – Web UI guide
- **[Deployment](docs/deployment.md)** – Production setup

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License – See LICENSE file for details

---

## 🎯 Roadmap

| Phase | Status | Features |
|-------|--------|----------|
| **Phase 1** | ✅ Complete | Text backend, LLM integration, chat API |
| **Phase 2** | 🚀 Active | Voice (STT/TTS), tools, plugin system |
| **Phase 3** | 📋 Planned | Vision, data analysis, dashboards |
| **Phase 4** | 📋 Planned | ML pipelines, autonomous workflows |

---

## ❓ FAQ

**Q: Can I run ROSE locally without cloud APIs?**  
A: Yes! Use local LLM models (Ollama) and Whisper for everything. Cloud is optional.

**Q: How do I create a custom tool?**  
A: Tools go in `tools/` directory. See `docs/tools.md` for examples.

**Q: Can ROSE run autonomously without human oversight?**  
A: Yes, but `HUMAN_APPROVAL_REQUIRED=false` required. Use with caution!

**Q: Does ROSE support GPU acceleration?**  
A: Yes, configure LLM provider for GPU support.

**Q: Can I deploy ROSE on Kubernetes?**  
A: Yes! See `docs/deployment.md` for K8s setup.

---

## 🌟 Built with

- **FastAPI** – Modern Python web framework
- **SQLAlchemy** – Database ORM
- **PostgreSQL** – Relational database
- **OpenAI/Claude APIs** – Language models
- **Whisper** – Speech-to-text
- **Piper** – Text-to-speech
- **Plotly** – Interactive visualizations
- **Docker** – Container deployment
- **Kubernetes** – Orchestration

---

## 📞 Support

- 📧 Email: [support@rose-research.dev]
- 💬 Discussions: [GitHub Discussions](https://github.com/your-repo/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 📖 Docs: [Full Documentation](docs/)

---

**Built for researchers by researchers.** 🔬🚀

*ROSE – Because great research deserves great tools.*
