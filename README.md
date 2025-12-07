# **Simple Todo API \- DevOps Project**

## **📖 Overview**

This project is a RESTful backend service built with **FastAPI**, designed to demonstrate a complete DevOps lifecycle. It includes automated CI/CD pipelines, containerization, Kubernetes deployment, and full observability.

## **🚀 Key Features**

* **REST API:** Create, Read, Update, and Delete (CRUD) Todo items.  
* **CI/CD:** GitHub Actions pipeline for automated testing, security scanning (Bandit), and Docker build/push.  
* **Observability:** \- **Metrics:** Prometheus endpoint (/metrics) scraped by a Kubernetes Prometheus deployment.  
  * **Logs:** Structured JSON logging.  
  * **Tracing:** Unique Request IDs for transaction tracking.  
* **Infrastructure:** Kubernetes Deployment, NodePort Services, and ConfigMaps.

## **🛠️ Tech Stack**

* **Language:** Python 3.9 (FastAPI)  
* **Containerization:** Docker  
* **Orchestration:** Kubernetes (Minikube)  
* **CI/CD:** GitHub Actions  
* **Monitoring:** Prometheus

## **🏃‍♂️ How to Run**

### **1\. Local Development**

\# Install dependencies  
pip install \-r requirements.txt  
\# Run the app  
python app/main.py

Access the API at: http://localhost:8000

### **2\. Kubernetes Deployment**

\# Apply app and monitoring  
kubectl apply \-f k8s/

\# Access the Todo App  
kubectl port-forward svc/todo-app-service 8080:80

\# Access Prometheus Dashboard  
kubectl port-forward svc/prometheus-service 9090:9090

## **📡 API Endpoints**

| Method | Endpoint | Description |
| :---- | :---- | :---- |
| GET | / | Welcome message |
| GET | /metrics | Prometheus metrics |
| GET | /todos/ | List all todos |
| POST | /todos/ | Create a new todo |
