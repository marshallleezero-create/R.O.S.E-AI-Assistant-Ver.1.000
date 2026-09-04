# ROSE Development Guide Index

## 📖 Quick Navigation

**New to ROSE?** Start here:
1. Read [README.md](README.md) - Project overview
2. Follow [docs/QUICKSTART.md](docs/QUICKSTART.md) - Get server running
3. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - How it works

**Want to understand the code?**
- [docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md) - Component breakdown
- [backend/app/main.py](backend/app/main.py) - Entry point
- [backend/app/services/](backend/app/services/) - Business logic

**Ready to deploy?**
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment options
- [DEVELOPMENT_CHECKLIST.md](DEVELOPMENT_CHECKLIST.md) - Build phases
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Current state

---

## 📁 Document Map

### Getting Started
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [README.md](README.md) | Project overview | 5 min |
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | Installation & first steps | 10 min |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | What's been built | 10 min |

### Technical Documentation
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design & components | 15 min |
| [docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md) | Code explanation | 20 min |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment | 20 min |

### Planning & Tracking
| Document | Purpose | Read Time |
|----------|---------|-----------|
| [DEVELOPMENT_CHECKLIST.md](DEVELOPMENT_CHECKLIST.md) | All phases & tasks | 15 min |

---

## 🏗️ Project Structure

```
R.O.S.E-AI-Assistant-Ver.1.000/
│
├── README.md                          # Start here
├── PROJECT_STATUS.md                  # Current progress
├── DEVELOPMENT_CHECKLIST.md           # All tasks
│
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── config.py                  # Settings
│   │   ├── database.py                # SQLAlchemy ORM
│   │   ├── services/
│   │   │   ├── llm.py                 # LLM integration
│   │   │   └── agent.py               # Agent orchestration
│   │   └── routes/
│   │       ├── chat.py                # Chat API
│   │       ├── experiments.py         # Experiments API
│   │       └── health.py              # Health checks
│   ├── tests/
│   │   └── test_api.py                # Test suite
│   └── requirements.txt               # Dependencies
│
├── frontend/                          # (Phase 1+) Web UI
│   ├── public/
│   └── src/
│
├── docs/
│   ├── ARCHITECTURE.md                # System design
│   ├── CODE_WALKTHROUGH.md            # Code explanation
│   ├── QUICKSTART.md                  # Getting started
│   └── DEPLOYMENT.md                  # Deployment guide
│
├── .env.example                       # Config template
└── .gitignore                         # Git ignore
```

---

## 🚀 Quick Start Commands

### First Time Setup
```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env
```

### Run Development Server
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### Test the API
```bash
# Health check
curl http://localhost:8000/health

# Create session
curl -X POST http://localhost:8000/api/chat/sessions

# Send message
curl -X POST http://localhost:8000/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello ROSE"}],
    "temperature": 0.7
  }'
```

### Run Tests
```bash
cd backend
pytest tests/ -v
```

---

## 📋 What's Included

### ✅ Phase 1: Text Brain (Complete)

**Backend Infrastructure**
- ✅ FastAPI REST API server
- ✅ SQLite database with ORM
- ✅ LLM service (Ollama + OpenAI)
- ✅ Agent orchestration framework
- ✅ Chat and experiment APIs
- ✅ Health checks and status

**Documentation**
- ✅ Architecture guide
- ✅ Code walkthrough
- ✅ Quick start guide
- ✅ Deployment guide
- ✅ Development checklist

**Configuration**
- ✅ Environment variables
- ✅ Flexible LLM provider selection
- ✅ Database path configuration
- ✅ Logging setup

**Testing**
- ✅ Basic API tests
- ✅ Health check tests
- ✅ Session management tests
- ✅ Experiment creation tests

---

## 🎯 Next Steps by Role

### If You're a Developer
1. Read [docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md)
2. Pick a task from [DEVELOPMENT_CHECKLIST.md](DEVELOPMENT_CHECKLIST.md)
3. Follow [docs/QUICKSTART.md](docs/QUICKSTART.md) to get running
4. Check [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design

### If You're a Researcher
1. Read [README.md](README.md) for overview
2. Follow [docs/QUICKSTART.md](docs/QUICKSTART.md) to install
3. Try the chat API (see commands above)
4. Read [PROJECT_STATUS.md](PROJECT_STATUS.md) for features

### If You're Deploying
1. Read [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
2. Choose deployment method (Docker, cloud, local)
3. Configure environment variables
4. Follow deployment instructions

### If You're Contributing
1. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design
2. Read [DEVELOPMENT_CHECKLIST.md](DEVELOPMENT_CHECKLIST.md) for tasks
3. Pick a feature to implement
4. Follow code style in [docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md)

---

## 🔧 Configuration

### Basic Setup (.env)
```env
# Use local Ollama (free)
LLM_PROVIDER=ollama
LLM_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434

# OR use OpenAI (paid, better)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

See [.env.example](.env.example) for all options.

---

## 📚 Key Concepts

### Architecture Layers
1. **Interface**: REST API (FastAPI)
2. **Services**: Business logic (LLM, Agent)
3. **Data**: Database (SQLite/PostgreSQL)
4. **Tools**: External integrations (Phase 2+)

### Request Flow
```
HTTP Request → FastAPI Route → Service Layer → LLM/Database → Response
```

### Phases
- **Phase 1**: Text reasoning (✅ Done)
- **Phase 2**: Voice + tools (📋 Planned)
- **Phase 3**: Vision + analysis (📋 Future)
- **Phase 4**: ML + automation (📋 Future)

---

## 💡 Tips

### For Local Development
- Use `--reload` flag with uvicorn for hot reloading
- Set `DEBUG=True` in `.env` for verbose logging
- Use SQLite (default) for simplicity
- Check `logs/rose.log` for error details

### For Production
- Set `DEBUG=False`
- Use PostgreSQL instead of SQLite
- Set `SECRET_KEY` to a random value
- Configure CORS properly
- Use environment variables for secrets
- Set up monitoring/logging

### For Performance
- Use Ollama locally for fast responses
- Use OpenAI only for complex tasks
- Add database indexes
- Implement caching (Phase 2+)
- Use streaming for long outputs

---

## ❓ Troubleshooting

### Can't connect to Ollama
```bash
# Make sure Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### Database errors
```bash
# Reset database
rm data/rose.db
# Restart server—it will recreate the DB
```

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000
kill -9 <PID>
```

### More help?
See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) troubleshooting section

---

## 📖 Documentation Map (Detailed)

### Architecture
| File | Contains |
|------|----------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, components, dataflow |
| [docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md) | Code explanation, patterns, examples |

### Getting Started
| File | Contains |
|------|----------|
| [README.md](README.md) | Project overview, quick links |
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | Installation, configuration, first API call |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | What's been built, status, next steps |

### Deployment
| File | Contains |
|------|----------|
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Docker, cloud, systemd, monitoring |
| [.env.example](.env.example) | Configuration options |

### Planning
| File | Contains |
|------|----------|
| [DEVELOPMENT_CHECKLIST.md](DEVELOPMENT_CHECKLIST.md) | All tasks by phase, quality checklist |

---

## 🎓 Learning Resources

### Understanding ROSE
1. **Architecture first**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. **Then the code**: [docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md)
3. **Then run it**: [docs/QUICKSTART.md](docs/QUICKSTART.md)

### Understanding LLMs
- Ollama: https://ollama.ai (easy setup)
- Hugging Face: https://huggingface.co (model hub)
- LangChain: https://python.langchain.com (agent frameworks)

### Understanding FastAPI
- Official docs: https://fastapi.tiangolo.com
- Tutorial: https://fastapi.tiangolo.com/tutorial/

---

## 🎉 You're Ready!

Everything is set up. Pick a task and start building:

1. **Run the server** → Follow [docs/QUICKSTART.md](docs/QUICKSTART.md)
2. **Understand the code** → Read [docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md)
3. **Plan next features** → Check [DEVELOPMENT_CHECKLIST.md](DEVELOPMENT_CHECKLIST.md)
4. **Deploy to production** → Follow [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

Questions? Check the specific guide above, or look at the code—it's well-commented!

---

**Happy coding!** 🌹🚀
