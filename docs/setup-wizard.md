# Setup Wizard

ROSE includes an interactive CLI setup wizard that guides you through configuration.

## What It Does

The setup wizard generates:

✅ `config.yaml` – Main configuration  
✅ `secrets.env` – API keys and credentials  
✅ `plugins/` directory – Plugin structure  
✅ `data/` directory – Data storage  
✅ Example plugin – Template for development  

## Running the Wizard

```bash
python setup_wizard.py
```

You'll be guided through these sections:

### 1. Database Configuration

Choose your database:

- **PostgreSQL** (recommended for production)
  - Specify host, port, username, password, database name
  - Example: `postgresql://rose:password@localhost:5432/rose_db`

- **SQLite** (quick for local development)
  - File-based, no setup needed
  - Example: `sqlite:///./data/rose.db`

### 2. LLM Provider

Select your language model provider:

- **Ollama** (local, free, private)
  - Server URL: `http://localhost:11434`
  - Download: https://ollama.ai
  - No API key needed

- **OpenAI** (cloud, powerful, paid)
  - Requires API key: `sk-...`
  - Visit: https://platform.openai.com/account/api-keys

- **Claude** (cloud, excellent reasoning, paid)
  - Requires API key
  - Visit: https://www.anthropic.com

### 3. Vision & Voice (Optional)

Enable multimodal capabilities:

- **Vision** – Image analysis
  - Provider: OpenAI or local
  - API key if using cloud

- **Whisper** (Speech-to-Text)
  - Command: `whisper`
  - Install: `pip install openai-whisper`

- **Piper** (Text-to-Speech)
  - Command: `piper`
  - Install: `pip install piper-tts`

### 4. Autonomy Mode (Optional)

Enable autonomous research workflows:

- Self-directed experiment planning
- Automatic execution and analysis
- Human approval gates (optional)
- Max iterations to prevent runaway execution

### 5. API Configuration

Basic API settings:

- **Host** – `0.0.0.0` (accessible externally) or `localhost` (local only)
- **Port** – Default 8000
- **Debug** – Enable verbose logging

## Configuration Files

### config.yaml

Main configuration file (human-readable):

```yaml
database:
  url: postgresql://rose:rose@localhost/rose_db
  echo: false

llm:
  provider: ollama
  url: http://localhost:11434
  api_key: ${LLM_API_KEY}

vision:
  enabled: true
  provider: openai
  url: https://api.openai.com/v1/vision
  api_key: ${VISION_API_KEY}

voice:
  whisper_enabled: true
  whisper_command: whisper
  piper_enabled: true
  piper_command: piper

autonomy:
  enabled: false
  max_iterations: 10
  human_approval_required: true

api:
  host: 0.0.0.0
  port: 8000
  debug: false
```

### secrets.env

Credentials file (⚠️ keep safe!):

```env
LLM_API_KEY=sk-...
VISION_API_KEY=sk-...
```

**Important:** Never commit this file to version control!

Add to `.gitignore`:
```
secrets.env
```

## Environment Variables

ROSE reads configuration from:

1. **config.yaml** – Main settings
2. **secrets.env** – Sensitive credentials
3. **Environment variables** – Overrides (if set)

Precedence: Environment > Secrets > Config

## Reconfiguring

To reconfigure after initial setup:

```bash
# Wizard will overwrite existing files
python setup_wizard.py

# Or manually edit config.yaml
nano config.yaml

# Then restart ROSE
uvicorn main:app --reload
```

## Wizard Features

- ✅ Interactive prompts with sensible defaults
- ✅ Input validation
- ✅ Directory creation
- ✅ Example plugin generation
- ✅ Secure permissions for secrets file
- ✅ Configuration summary
- ✅ Next steps guidance

## Common Configurations

### Local Development (SQLite + Ollama)

```
Database: sqlite
LLM: ollama
Vision: disabled
Autonomy: disabled
```

Command: `ollama serve` (in another terminal)

### Production (PostgreSQL + OpenAI)

```
Database: postgresql
LLM: openai
Vision: enabled (openai)
Autonomy: enabled (human approval)
```

### Research Lab (PostgreSQL + Local + Cloud Fallback)

```
Database: postgresql
LLM: ollama (local first)
Vision: local or openai
Autonomy: enabled
```

## Troubleshooting

### Wizard crashes

Try running with Python explicitly:
```bash
python3 setup_wizard.py
```

### Database connection fails

Verify PostgreSQL:
```bash
psql -h localhost -U rose -d rose_db
```

Or switch to SQLite temporarily.

### LLM not responding

Check Ollama or API key:
```bash
# Ollama
ollama serve
ollama pull llama2

# OpenAI
echo $OPENAI_API_KEY  # Should not be empty
```

### Secrets file has wrong permissions

Fix with:
```bash
chmod 600 secrets.env
```

---

**Next:** [Architecture Overview](architecture.md)
