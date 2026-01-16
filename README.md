# Simple Todo API - DevOps Project

Welcome to the Simple Todo API project! This is a lightweight REST application built to demonstrate core DevOps practices including CI/CD, Containerization, Kubernetes, Observability, and Security.

##  Project Overview

This project implements a simple backend service for managing Todo items. It meets the following objectives:
- **Backend**: Python (FastAPI) implementation under 150 lines.
- **Containerization**: Dockerized application optimized for size.
- **Orchestration**: Kubernetes manifests for deployment (Deployment & Service).
- **CI/CD**: GitHub Actions pipeline for testing, security scanning, and building.
- **Observability**: Prometheus metrics, structured logging, and request tracing.
- **Security**: SAST (Bandit) and DAST (OWASP ZAP) scans.

---

##  Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (optional, for local dev without Docker)
- Kubernetes (Minikube or Kind)

### 1 Run Locally (Docker Compose)
The easiest way to run the app is with Docker Compose.
```bash
docker-compose up --build
```
The app will be available at [http://localhost:8000](http://localhost:8000).

### 2 Run Locally (Python)
If you prefer running it directly on your machine:
```bash
# Create virtual env
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload
```

---

##  Security Scans

We take security seriously! This project implements both SAST and DAST.

### Static Analysis (SAST)
We use **Bandit** to check for common security issues in Python code.
```bash
bandit -r app/
```

### Dynamic Analysis (DAST)
We use **OWASP ZAP** to scan the running application for vulnerabilities.
Run the provided script to start a scan against your local instance:
```bash
./run_dast.sh
```
*Note: Make sure the app is running (via Docker or Python) before scanning.*
The report will be saved in the `zap_reports/` directory.

---

##  Observability

### Metrics
Prometheus metrics are exposed at `/metrics`. You can scrape them using a Prometheus server.

### Logging & Tracing
Every request is logged with a unique `X-Request-ID`.
- Check the console output heavily for structured logs.
- The `X-Request-ID` is returned in the response headers for tracking.

---

##  Kubernetes Deployment

To deploy to a running Minikube cluster:

1. **Apply Manifests**:
   ```bash
   kubectl apply -f k8s/
   ```

2. **Access the App**:
   ```bash
   # If using NodePort (default setup)
   minikube service todo-app-service --url
   ```

---

##  API Examples

### Create a Todo
```bash
curl -X POST "http://localhost:8000/todos/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Finish DevOps Project", "description": "Write final report", "completed": false}'
```

### Javascript Fetch Example
```javascript
fetch('http://localhost:8000/todos/')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

##  Author
Built for the DevOps course requirements. 
*Enjoy the journey, not just the destination.*
