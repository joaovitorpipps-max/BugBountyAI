"""Installation Guide untuk BugBountyAI v2 + Gemini AI"""

# 🚀 BugBountyAI v2 - Installation Guide

## Prerequisites
- Python 3.11+ (TensorFlow support)
- pip atau poetry
- Git
- Google Gemini API Key (untuk AI features)

---

## Installation Options

### Option 1: Minimal Installation (Recommended untuk Python 3.14)

```bash
# 1. Clone repository
git clone https://github.com/joaovitorpipps-max/BugBountyAI.git
cd BugBountyAI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# 3. Install minimal dependencies (Python 3.14 compatible)
pip install -r requirements-minimal.txt

# 4. Test installation
python -c "from bugbountyai import BugBountyAnalyzer; print('✅ Installation successful!')"
```

### Option 2: Full Installation (Python 3.11/3.12)

```bash
# Untuk Python 3.11 atau 3.12 (dengan ML capabilities)
pip install -r requirements-python314.txt
```

### Option 3: Docker Installation (Recommended)

```bash
# 1. Build image
docker build -t bugbountyai:v2 .

# 2. Run container
docker run -p 8000:8000 bugbountyai:v2

# API available at http://localhost:8000
```

### Option 4: Docker Compose (Full Stack)

```bash
# 1. Start all services
docker-compose up -d

# 2. Check services
docker-compose ps

# Services:
# - API: http://localhost:8000
# - Database: localhost:5432
# - Redis: localhost:6379
```

---

## Quick Start

### 1. Setup Gemini API Key

```bash
# Create .env file
cp .env.gemini.example .env.gemini

# Edit .env.gemini dan masukkan Gemini API Key
GEMINI_API_KEY=your-gemini-api-key-here
```

### 2. Test Basic Scan

```bash
# Without Gemini AI
python -m bugbountyai.cli.main scan https://example.com

# With Gemini AI
python -m bugbountyai.cli.gemini_cli scan-gemini https://example.com --gemini-key YOUR_KEY
```

### 3. Test API

```bash
# Start API server
uvicorn bugbountyai.api.v2_api:app --reload

# In another terminal, test health check
curl http://localhost:8000/api/v2/health
```

---

## Troubleshooting

### Python 3.14 Compatibility Issues

**Problem:** `tensorflow` tidak support Python 3.14

**Solution:** Gunakan `requirements-minimal.txt`

```bash
pip install -r requirements-minimal.txt
```

### Gemini API Key Issues

**Problem:** `google-generativeai` error

**Solution:** 
```bash
# Install latest version
pip install --upgrade google-generativeai

# Verify API key
echo $GEMINI_API_KEY
```

### Module Import Errors

**Problem:** `ModuleNotFoundError: No module named 'bugbountyai'`

**Solution:**
```bash
# Install in development mode
pip install -e .
```

### Database Connection Errors

**Problem:** PostgreSQL connection failed

**Solution:**
```bash
# Use Docker database
docker-compose up -d db

# Or use local database
sudo service postgresql start
```

---

## Verify Installation

```bash
# Check version
python -c "import bugbountyai; print(f'BugBountyAI {bugbountyai.__version__}')"

# Check Gemini integration
python -c "from bugbountyai.ai.gemini_analyzer import GeminiAIAnalyzer; print('✅ Gemini AI ready')"

# Check CLI
bugbountyai --version
```

---

## Running Scans

### CLI Scan
```bash
bugbountyai scan https://target.com --deep --report pdf --output report.pdf
```

### CLI Scan with Gemini AI
```bash
bugbountyai scan-gemini https://target.com --gemini-key YOUR_KEY --report pdf
```

### Python API
```python
from bugbountyai import BugBountyAnalyzer

analyzer = BugBountyAnalyzer(api_key="default")
results = analyzer.analyze_target("https://target.com")
print(results)
```

### REST API
```bash
# Start server
uvicorn bugbountyai.api.v2_api:app

# In another terminal
curl -X POST http://localhost:8000/api/v2/analysis/scan \
  -H "Content-Type: application/json" \
  -d '{"target_url":"https://target.com"}'
```

---

## Production Deployment

### Docker Production
```bash
# Build production image
docker build -t bugbountyai:v2-prod --target production .

# Run with env file
docker run -p 8000:8000 --env-file .env.production bugbountyai:v2-prod
```

### Kubernetes
```bash
# Deploy to Kubernetes
kubectl apply -f k8s-deployment.yaml

# Check deployment
kubectl get pods
kubectl logs deployment/bugbountyai-api
```

---

## Next Steps

1. ✅ Install BugBountyAI
2. ✅ Setup Gemini API Key
3. ✅ Run first scan
4. ✅ View report
5. ✅ Deploy to production

**Happy scanning! 🚀**
