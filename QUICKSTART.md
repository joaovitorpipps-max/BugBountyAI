"""Quick Start Guide untuk BugBountyAI v2"""

# 🚀 BugBountyAI v2 - Quick Start Guide

## Installation

### Option 1: Install from PyPI
```bash
pip install bugbountyai
```

### Option 2: Install from Source
```bash
git clone https://github.com/joaovitorpipps-max/BugBountyAI.git
cd BugBountyAI
pip install -e .
```

### Option 3: Docker
```bash
docker build -t bugbountyai:v2 .
docker run -p 8000:8000 bugbountyai:v2
```

---

## Usage

### 1️⃣ Basic URL Scanning
```bash
bugbountyai scan https://target.com
```

### 2️⃣ Deep Scanning with Auto-Exploitation
```bash
bugbountyai scan https://target.com --deep --exploit --report pdf
```

### 3️⃣ Code Security Analysis
```bash
bugbountyai code-scan /path/to/code
```

### 4️⃣ Real-time Monitoring
```bash
bugbountyai monitor https://target1.com https://target2.com --interval 600
```

### 5️⃣ Connect to HackerOne
```bash
bugbountyai connect --platform hackerone
```

### 6️⃣ Submit Report
```bash
bugbountyai submit analysis_123 --platform hackerone --program-id h1_program
```

---

## API Usage

### Python Example
```python
from bugbountyai import BugBountyAnalyzer

# Initialize
analyzer = BugBountyAnalyzer(api_key="your-api-key")

# Scan target
results = analyzer.analyze_target("https://target.com", deep_scan=True)

# Print results
print(f"Risk Score: {results['risk_score']}/100")
print(f"Vulnerabilities Found: {len(results['vulnerabilities'])}")

# Generate report
report_path = analyzer.generate_report(results, format="pdf")
print(f"Report: {report_path}")
```

### REST API Example
```bash
# Login
curl -X POST http://localhost:8000/api/v2/auth/login \
  -d '{"username":"user","password":"pass"}'

# Start scan
curl -X POST http://localhost:8000/api/v2/analysis/scan \
  -H "Authorization: Bearer TOKEN" \
  -d '{"target_url":"https://target.com","deep_scan":true}'

# Get results
curl http://localhost:8000/api/v2/analysis/analysis_123 \
  -H "Authorization: Bearer TOKEN"
```

### WebSocket Example
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/analysis_123');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Update:', data);
};

// Subscribe to alerts
ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'alerts'
}));
```

---

## Configuration

```bash
bugbountyai config
```

This will create `.bugbountyai_config` with:
```json
{
  "api_url": "http://localhost:8000",
  "api_key": "your-api-key",
  "webhook_url": "https://your-webhook.com/alerts",
  "report_format": "pdf"
}
```

---

## Docker Compose (Full Stack)

```bash
# Start all services
docker-compose up -d

# API will be available at http://localhost:8000
# Database: PostgreSQL at localhost:5432
# Cache: Redis at localhost:6379

# Check logs
docker-compose logs -f api
```

---

## Kubernetes Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s-deployment.yaml

# Check status
kubectl get pods
kubectl get svc bugbountyai-service

# Port forward
kubectl port-forward svc/bugbountyai-service 8000:80
```

---

## Features at a Glance

✅ **Reconnaissance** - Auto gather domain info, technologies, endpoints
✅ **Vulnerability Scanning** - Detect SQL Injection, XSS, CSRF, LFI, SSRF, etc
✅ **Deep Learning Analysis** - Predict vulnerabilities using ML models
✅ **Auto-Exploitation** - Automatically exploit vulnerabilities with POC
✅ **Risk Scoring** - CVSS scoring for each vulnerability
✅ **Real-time Monitoring** - Continuous scanning with alerts
✅ **Platform Integration** - HackerOne & Bugcrowd auto-submission
✅ **Professional Reports** - OWASP, PCI-DSS, HIPAA compliance reports
✅ **Multi-User** - Team collaboration with role-based access
✅ **Audit Logging** - Full activity tracking
✅ **REST API v2** - Full-featured API with JWT authentication
✅ **WebSocket** - Real-time updates
✅ **GraphQL Scanning** - Detect GraphQL vulnerabilities
✅ **Mobile App Testing** - Analyze mobile app security
✅ **Cloud Scanning** - AWS, Azure, GCP infrastructure analysis
✅ **Fuzzing Engine** - Intelligent mutation-based fuzzing
✅ **Database Testing** - MongoDB, MySQL, PostgreSQL security scanning

---

## Performance

- ⚡ Scan Speed: 5-30 seconds (standard), 30-120 seconds (deep)
- 🧠 ML Processing: Real-time with GPU acceleration (optional)
- 💾 Database: PostgreSQL with Redis caching
- 🔄 Concurrent Scans: Up to 100+ simultaneous targets
- 📊 Reporting: Generate in <5 seconds

---

## Support & Documentation

- 📖 [Full Documentation](docs/)
- 🐛 [Report Issues](https://github.com/joaovitorpipps-max/BugBountyAI/issues)
- 💬 [Discussions](https://github.com/joaovitorpipps-max/BugBountyAI/discussions)
- 📧 [Email Support](mailto:team@bugbountyai.com)

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Disclaimer

⚠️ **This tool is for authorized security testing only.**

Unauthorized access to computer systems is illegal. Only use BugBountyAI on systems you own or have explicit permission to test.

---

**Ready to find vulnerabilities? Start scanning! 🚀**

```bash
bugbountyai scan https://your-target.com
```
