"""Comprehensive Documentation untuk BugBountyAI v2"""

# 📚 BugBountyAI v2 - Complete Documentation

## Table of Contents
1. [Installation](#installation)
2. [CLI Commands](#cli-commands)
3. [API Reference](#api-reference)
4. [Configuration](#configuration)
5. [Advanced Features](#advanced-features)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## Installation

### System Requirements
- Python 3.9+
- 4GB RAM minimum (8GB recommended)
- 2GB disk space
- Internet connection

### Quick Install
```bash
pip install bugbountyai
bugbountyai version
```

---

## CLI Commands

### scan
Perform security vulnerability scan on target URL

```bash
bugbountyai scan <URL> [OPTIONS]
```

**Options:**
- `--deep` - Enable deep scanning (slower, more thorough)
- `--exploit` - Automatically exploit found vulnerabilities
- `--report {pdf|html|json}` - Report format (default: pdf)
- `--output <PATH>` - Save report to specific path

**Examples:**
```bash
# Basic scan
bugbountyai scan https://example.com

# Deep scan with exploitation
bugbountyai scan https://example.com --deep --exploit

# Save as JSON report
bugbountyai scan https://example.com --report json --output report.json
```

---

### code-scan
Analyze source code for security vulnerabilities

```bash
bugbountyai code-scan <PATH> [OPTIONS]
```

**Options:**
- `--output <PATH>` - Save report to specific path

**Examples:**
```bash
bugbountyai code-scan /path/to/code
bugbountyai code-scan /path/to/code --output code_report.json
```

---

### monitor
Start continuous real-time monitoring

```bash
bugbountyai monitor <URL1> <URL2> ... [OPTIONS]
```

**Options:**
- `--interval <SECONDS>` - Scan interval (default: 300)
- `--webhook <URL>` - Webhook URL for alerts

**Examples:**
```bash
# Monitor single target every 10 minutes
bugbountyai monitor https://example.com --interval 600

# Monitor multiple targets with webhook
bugbountyai monitor https://site1.com https://site2.com \
  --webhook https://your-server.com/webhook
```

---

### connect
Connect to bug bounty platforms

```bash
bugbountyai connect --platform {hackerone|bugcrowd}
```

**Interactive Setup:**
```bash
bugbountyai connect --platform hackerone
# Enter API Token when prompted
# Enter Username when prompted
```

---

### submit
Submit vulnerability report to platform

```bash
bugbountyai submit <ANALYSIS_ID> --platform <PLATFORM> --program-id <ID>
```

**Examples:**
```bash
bugbountyai submit analysis_123 --platform hackerone --program-id h1_12345
```

---

### config
Manage BugBountyAI configuration

```bash
bugbountyai config
```

Interactive configuration setup for:
- API URL
- API Key
- Webhook URL
- Default report format

---

## API Reference

### Authentication

All API requests require JWT token:

```bash
curl -X POST http://localhost:8000/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### Analysis Endpoints

#### POST /api/v2/analysis/scan
Start new vulnerability scan

```bash
curl -X POST http://localhost:8000/api/v2/analysis/scan \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://example.com",
    "deep_scan": false,
    "include_exploit": false,
    "generate_report": true
  }'
```

Response:
```json
{
  "analysis_id": "analysis_1693123456",
  "target": "https://example.com",
  "status": "queued",
  "created_at": "2024-08-27T10:00:00",
  "estimated_completion": "2024-08-27T10:30:00"
}
```

#### GET /api/v2/analysis/{analysis_id}
Get analysis results

```bash
curl http://localhost:8000/api/v2/analysis/analysis_123 \
  -H "Authorization: Bearer TOKEN"
```

Response:
```json
{
  "analysis_id": "analysis_123",
  "status": "completed",
  "vulnerabilities": [
    {
      "type": "SQL Injection",
      "severity": "high",
      "description": "Potential SQL injection in login form",
      "endpoint": "/login",
      "confidence": 0.95
    }
  ],
  "risk_score": 75.5,
  "timestamp": "2024-08-27T10:00:00"
}
```

---

### Exploitation Endpoints

#### POST /api/v2/exploitation/auto-exploit
Automatically exploit vulnerabilities

```bash
curl -X POST http://localhost:8000/api/v2/exploitation/auto-exploit \
  -H "Authorization: Bearer TOKEN" \
  -d 'analysis_id=analysis_123'
```

#### GET /api/v2/exploitation/{exploitation_id}/poc
Get proof of concept code

```bash
curl "http://localhost:8000/api/v2/exploitation/exp_123/poc?language=python" \
  -H "Authorization: Bearer TOKEN"
```

---

### Monitoring Endpoints

#### POST /api/v2/monitoring/start
Start real-time monitoring

```bash
curl -X POST http://localhost:8000/api/v2/monitoring/start \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "targets": ["https://target1.com", "https://target2.com"],
    "interval": 300
  }'
```

#### GET /api/v2/monitoring/{monitoring_id}/alerts
Get monitoring alerts

```bash
curl "http://localhost:8000/api/v2/monitoring/monitor_123/alerts?severity=critical" \
  -H "Authorization: Bearer TOKEN"
```

---

### Integration Endpoints

#### POST /api/v2/integration/hackerone
Connect to HackerOne

```bash
curl -X POST http://localhost:8000/api/v2/integration/hackerone \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "hackerone",
    "program_id": "h1_12345",
    "api_token": "your_token"
  }'
```

#### POST /api/v2/integration/submit-report
Submit report to platform

```bash
curl -X POST http://localhost:8000/api/v2/integration/submit-report \
  -H "Authorization: Bearer TOKEN" \
  -d 'analysis_id=analysis_123&platform=hackerone&program_id=h1_12345'
```

---

### Reporting Endpoints

#### POST /api/v2/reports/generate
Generate security report

```bash
curl -X POST http://localhost:8000/api/v2/reports/generate \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_id": "analysis_123",
    "format": "pdf",
    "template": "owasp"
  }'
```

---

## Configuration

### Environment Variables

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
API_WORKERS=4

# Database
DATABASE_URL=postgresql://user:password@localhost/bugbountyai

# Cache
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/bugbountyai.log

# Features
ENABLE_DEEP_SCAN=true
ENABLE_AUTO_EXPLOIT=true
ENABLE_MONITORING=true
```

### Configuration File

`.bugbountyai_config`:
```json
{
  "api_url": "http://localhost:8000",
  "api_key": "your-api-key",
  "webhook_url": "https://your-webhook.com/alerts",
  "report_format": "pdf",
  "scan_timeout": 3600,
  "deep_scan_enabled": true,
  "auto_exploit_enabled": true
}
```

---

## Advanced Features

### Deep Learning Models
- VulnerabilityDL-v2
- Transfer Learning from pre-trained models
- Zero-day pattern detection

### Automated Exploitation
- SQL Injection exploitation
- XSS payload injection
- RCE command execution
- LFI path traversal
- SSRF requests
- Exploit chaining

### GraphQL Scanning
```bash
bugbountyai scan https://api.example.com/graphql --deep
```

### Mobile App Testing
```python
from bugbountyai.scanning.advanced_scanner import AdvancedScanner

scanner = AdvancedScanner()
issues = scanner.scan_mobile_app("com.example.app")
```

### Cloud Infrastructure
```python
results = scanner.scan_cloud_infrastructure(
    provider="aws",
    credentials={"access_key": "...", "secret_key": "..."}
)
```

---

## Deployment

### Docker
```bash
docker build -t bugbountyai:v2 .
docker run -p 8000:8000 -e API_DEBUG=false bugbountyai:v2
```

### Docker Compose
```bash
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f k8s-deployment.yaml
```

---

## Troubleshooting

### Connection Issues
```bash
# Test API connectivity
curl http://localhost:8000/api/v2/health

# Check logs
docker-compose logs api
```

### Database Issues
```bash
# Reset database
psql -U user -d bugbountyai -f reset.sql

# Check connections
psql -U user -d bugbountyai -c "SELECT version();"
```

### Performance Issues
```bash
# Check Redis cache
redis-cli ping

# Monitor resources
docker stats bugbountyai
```

---

**For more help, visit:** https://github.com/joaovitorpipps-max/BugBountyAI
