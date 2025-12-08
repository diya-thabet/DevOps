# Simple Todo App - DevOps Project

This is a **FastAPI** based Todo Application designed to demonstrate core **DevOps** practices including **Dockerizing applications**, **Kubernetes orchestration**, **CI/CD pipelines**, and **Observability** with Prometheus.

## 🚀 Project Overview

The project consists of:
- **FastAPI Application**: A REST API for managing Todos (with in-memory storage).
- **Docker**: Containerized application for consistent deployment.
- **Docker Compose**: Tool to run the application locally with hot-reloading.
- **Kubernetes**: Manifests to deploy the application and Prometheus monitoring stack to a cluster.
- **Prometheus**: Monitoring solution to scrape metrics from the application.
- **GitHub Actions**: CI/CD pipeline for testing, security scanning, and building Docker images.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.9+** (for local development)
2.  **Docker** (for containerization)
3.  **Docker Compose** (for local orchestration)
4.  **Minikube** (or any Kubernetes cluster)
5.  **kubectl** (Kubernetes CLI)
6.  **Git** (Version Control)

---

## 💻 Local Development

Run the application locally using Python.

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    Access the API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Docker Instructions

### 1. Build the Docker Image
```bash
docker build -t simple-todo-app:latest .
```

### 2. Run the Container
```bash
docker run -d -p 8000:8000 --name my-todo-app simple-todo-app:latest
```

### 3. Using Docker Compose (Recommended for Dev)
This method enables **hot-reloading**. If you change code in `app/`, it updates instantly.
```bash
docker-compose up --build
```
Access the app at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## ☸️ Kubernetes Deployment

Deploy the application to a local Minikube cluster.

### 1. Start Minikube
```bash
minikube start
```

### 2. Load Image into Minikube
Since we are building locally, we need to load the image into Minikube's Docker daemon.
```bash
minikube image load simple-todo-app:latest
```

### 3. Deploy Resources
Apply all manifests in the `k8s/` directory (Deployment, Service, Prometheus, etc.).
```bash
kubectl apply -f k8s/
```

### 4. Verify Deployment
Check if pods are running:
```bash
kubectl get pods
```

### 5. Access the App
The service uses `NodePort`. You can access it via minikube service command or port-forwarding.

**Option A: Minikube Service URL**
```bash
minikube service todo-app-service --url
```

**Option B: Port Forwarding (Universal)**
```bash
kubectl port-forward svc/todo-app-service 30007:80
```
Then go to [http://localhost:30007/docs](http://localhost:30007/docs).

---

## 📊 Monitoring with Prometheus

Prometheus is configured to scrape metrics from the application automatically.

1.  **Access Prometheus Dashboard:**
    ```bash
    # Forward the Prometheus service port
    kubectl port-forward svc/prometheus-service 9090:9090
    ```
    Open [http://localhost:9090](http://localhost:9090) in your browser.

2.  **Query Metrics:**
    Type `http_requests_total` in the query bar to see request counts for the Todo App.

---

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow in `.github/workflows/pipeline.yml` that automatically:
1.  **Tests**: Runs `pytest`.
2.  **Scans**: Runs `bandit` for security vulnerabilities.
3.  **Builds & Pushes**: Builds the Docker image and pushes to Docker Hub (on push to `main`).

---

## 🧪 Testing

Run unit tests locally:
```bash
pytest
```
