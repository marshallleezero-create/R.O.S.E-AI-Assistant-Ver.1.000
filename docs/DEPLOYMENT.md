# Deployment Guide

## Development Setup

### Local Development

```bash
# 1. Clone repo
git clone <repo-url>
cd R.O.S.E-AI-Assistant-Ver.1.000

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Configure environment
cp ../.env.example .env
# Edit .env with your settings

# 5. Start development server
python -m uvicorn app.main:app --reload --port 8000
```

### With Ollama (Local LLM)

```bash
# In separate terminal
ollama pull llama2  # or your preferred model
ollama serve

# In your .env
LLM_PROVIDER=ollama
LLM_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

## Production Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY .env.example .env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t rose:latest .
docker run -p 8000:8000 -v $(pwd)/data:/app/data rose:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  rose-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      LLM_PROVIDER: ollama
      OLLAMA_BASE_URL: http://ollama:11434
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
```

```bash
docker-compose up -d
```

### Cloud Deployment (AWS/GCP/Azure)

#### AWS (EC2)
1. Launch EC2 instance (Ubuntu 22.04)
2. Install Python 3.11+
3. Clone repo and follow development setup
4. Use systemd to run as service
5. Configure security groups for port 8000

#### AWS Lambda + API Gateway
- Package app using Mangum
- Deploy requirements.txt to Lambda layer
- Provide API Gateway endpoint

#### Google Cloud Run
```bash
gcloud run deploy rose-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="LLM_PROVIDER=openai,OPENAI_API_KEY=$OPENAI_KEY"
```

### Systemd Service (Linux)

Create `/etc/systemd/system/rose.service`:
```ini
[Unit]
Description=ROSE AI Assistant
After=network.target

[Service]
Type=simple
User=rose
WorkingDirectory=/opt/rose
ExecStart=/opt/rose/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable rose
sudo systemctl start rose
sudo systemctl status rose
```

## Environment Configuration

### Cloud LLM (Recommended for Production)

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
OPENAI_API_KEY=sk-...

# OR for Claude
LLM_PROVIDER=openai  # (use LangChain adapter)
CLAUDE_API_KEY=sk-ant-...
```

### Local LLM (Cost-Free)

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

### Database

```env
# SQLite (default, file-based)
DB_PATH=./data/rose.db

# PostgreSQL (production)
DATABASE_URL=postgresql://user:pass@localhost/rose
```

## Monitoring & Logging

### Logging Configuration
```env
LOG_LEVEL=INFO
LOG_FILE=./logs/rose.log
```

### Health Checks
```bash
# Check API is running
curl http://localhost:8000/health

# Check component status
curl http://localhost:8000/status
```

### Metrics & Monitoring
- Use Prometheus for metrics
- Use ELK stack or Datadog for logs
- Set up alerts for errors/downtime

## Backup & Recovery

### Database Backup
```bash
# SQLite backup
cp data/rose.db data/rose.db.backup.$(date +%Y%m%d)

# PostgreSQL backup
pg_dump -U user rose > rose.sql
```

### Data Recovery
```bash
# Restore from backup
cp data/rose.db.backup.YYYYMMDD data/rose.db

# Reinitialize database
python -c "from app.database import init_db; init_db()"
```

## Performance Optimization

1. **Database**: Add indexes for frequent queries
2. **Caching**: Implement Redis for session caching
3. **LLM**: Use smaller models locally, cloud fallback for complex tasks
4. **API**: Add rate limiting, implement pagination
5. **Frontend**: Implement lazy loading, caching

## Security Considerations

1. **API Keys**: Store in environment variables, never commit
2. **CORS**: Configure for your frontend domain only
3. **Authentication**: Implement JWT/OAuth for user sessions
4. **HTTPS**: Use SSL/TLS in production
5. **Database**: Enable encryption at rest
6. **Input Validation**: Sanitize all user inputs

## Troubleshooting

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database locked
```bash
# Delete and reinitialize
rm data/rose.db
python -m uvicorn app.main:app --reload
```

### Ollama connection refused
- Ensure Ollama is running: `ollama serve`
- Check OLLAMA_BASE_URL in .env
- Test: `curl http://localhost:11434/api/tags`

### Memory issues
- Use smaller LLM model (tiny, base instead of large)
- Implement LRU cache for sessions
- Consider database pagination
