# 🚀 Agentic CI/CD Risk Simulation & Predictive Pipeline Defense

An autonomous, multi-layered CI/CD risk management system that combines **LangGraph Agentic Workflows**, **Retrieval-Augmented Generation (RAG)**, **Machine Learning Predictive Analytics**, and **Kubernetes Cloud-Native Infrastructure** to preemptively identify and mitigate continuous integration failures.

## 📌 Project Overview

In high-velocity software engineering teams, broken CI/CD pipelines waste cloud execution credits and delay deployment velocity. This project provides a two-tiered defense framework:

1. **Lightweight Predictive Machine Learning Classifier:** Evaluates pipeline metadata from historical workflow runs via the GitHub REST API to predict build failures prior to exhaustive test suite execution.
2. **Autonomous LangGraph + RAG AI Agent:** Ingests pipeline configuration files (`.yaml`) and failure build logs (`.txt`) stored in a **ChromaDB** vector database to generate targeted `pytest` regression suites for high-risk modules.
3. **Cloud-Native Kubernetes Deployment:** Containerized via Docker and deployed onto a local Kubernetes cluster (**Minikube**) using Deployment and NodePort Service manifests to benchmark end-to-end execution latency in an isolated cloud environment.

## 🏗️ System Architecture

```text
                                +-----------------------------+
                                | Developer Pushes Code / PR  |
                                +--------------+--------------+
                                               |
                                               v
                                +-----------------------------+
                                |  GitHub Actions REST API   |
                                +--------------+--------------+
                                               |
                                               v
                                +-----------------------------+
                                | ML Predictor (scikit-learn) |
                                |  Flags High Risk Pipelines |
                                +--------------+--------------+
                                               |
                                               v
                   +-------------------------------------------------------+
                   |          LangGraph Autonomous Agent Workflow          |
                   |                                                       |
                   |  [ Node 1: Vector Search ] (ChromaDB Configs & Logs)  |
                   |                           |                           |
                   |  [ Node 2: Risk Analysis ] (Gemini 3.6 Flash LLM)     |
                   |                           |                           |
                   |  [ Node 3: Test Synth ]    (pytest Code Generation)   |
                   +---------------------------+---------------------------+
                                               |
                                               v
                                +-----------------------------+
                                |  Kubernetes Cluster Pod     |
                                |  (Flask Service @ Port 5000)|
                                +-----------------------------+
```

## 🗂️ Project Structure

```text
agentic-cicd-risk/
│
├── agent/                         # Autonomous AI Brain (LangGraph + RAG)
│   ├── build_graph.py             # LangGraph workflow orchestration & Flask REST API
│   ├── graph_nodes.py             # Directed graph nodes (Retrieve, Analyze, Generate)
│   └── retrieval_store.py         # ChromaDB vector store builder & query engine
│
├── classifier/                    # Machine Learning Pipeline Failure Predictor
│   ├── fetch_github_data.py       # Ingests live runs from GitHub Actions REST API
│   ├── feature_engineering.py     # Feature extraction & z-score normalization
│   ├── train_classifier.py        # Trains Logistic Regression model & evaluates metrics
│   └── raw_runs_data.csv          # Dataset of historical pipeline executions
│
├── deployment/                    # Cloud Infrastructure Manifests
│   ├── Dockerfile                 # Container packaging definition
│   ├── k8s-deployment.yaml        # Kubernetes Deployment specification
│   └── k8s-service.yaml           # Kubernetes NodePort Service binding
│
├── benchmark/                     # Architectural Performance Benchmarking
│   ├── run_direct.py              # Bare-metal Python execution time profiler
│   ├── run_via_minikube.py        # Kubernetes cluster network endpoint benchmark
│   └── benchmark_results.json     # Consolidated timing metrics output
│
├── generated_tests/               # Auto-generated pytest regression output suites
├── sample_data/                   # CI configs (.yaml) and build logs (.txt)
├── results/                       # Classifier evaluation output metrics
├── RESULTS.md                     # Detailed empirical evaluation documentation
├── README.md                      # Primary project documentation
└── requirements.txt               # Python package dependencies
```

## ⚡ Quickstart Guide

### 1. Prerequisites & Virtual Environment

Ensure you are running inside a **Linux/WSL2** environment with **Python 3.10+**, **Docker**, and **Minikube** installed.

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/agentic-cicd-risk.git
cd agentic-cicd-risk

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY="your_actual_gemini_api_key"
GITHUB_TOKEN="your_actual_github_token"
```

> **Note:** Never commit your `.env` file or expose API keys in the repository.

### 3. Initialize Vector Store (RAG)

Build the ChromaDB persistent store from sample workflow YAML files and build log files:

```bash
python agent/retrieval_store.py
```

### 4. Fetch Data & Train ML Classifier

Pull historical runs from the GitHub REST API, engineer normalized duration and event features, and train the model:

```bash
# Fetch raw pipeline data
python classifier/fetch_github_data.py

# Train classifier and evaluate on 20% held-out test split
python classifier/train_classifier.py
```

### 5. Run Direct Execution Benchmark

Profile execution speed running natively on bare metal:

```bash
python benchmark/run_direct.py
```

## ☁️ Kubernetes Cluster Deployment & Benchmarking

### 1. Start Cluster & Build Container

```bash
# Boot Minikube
minikube start --cpus=2 --memory=4000

# Build image directly inside Minikube
minikube image build -t agentic-cicd-image:latest -f deployment/Dockerfile .
```

### 2. Deploy Manifests to Kubernetes

```bash
# Apply deployment and service
kubectl apply -f deployment/k8s-deployment.yaml
kubectl apply -f deployment/k8s-service.yaml

# Verify pod status
kubectl get pods
```

### 3. Benchmark Cluster Endpoint

Expose the NodePort service endpoint:

```bash
minikube service agentic-cicd-service --url
```

In a separate terminal window, run the endpoint benchmark script:

```bash
python benchmark/run_via_minikube.py
```

## 📊 Empirical Metrics Summary

| Evaluation Dimension            |                                         Metric / Output |
| ------------------------------- | ------------------------------------------------------: |
| **ML Failure Recall (Class 1)** | **0.67** — Successfully caught 67% of pipeline failures |
| **ML Model Accuracy**           |                                                **0.62** |
| **Direct Execution Time (Avg)** |                  **82.61 seconds** — 3 graph iterations |
| **Minikube Pod Latency (Avg)**  |        **66.17 seconds** — End-to-end cluster tunneling |

For the complete empirical breakdown and interview defense scripts, refer to [`RESULTS.md`](./RESULTS.md).

## 🔑 Key Technologies

* **Python 3.10+**
* **LangGraph**
* **RAG**
* **ChromaDB**
* **Gemini 3.6 Flash**
* **scikit-learn**
* **Logistic Regression**
* **pytest**
* **Flask**
* **Docker**
* **Kubernetes**
* **Minikube**
* **GitHub Actions REST API**

## 🎯 Core Capabilities

* Predictive CI/CD failure detection
* Historical pipeline analysis
* RAG-based retrieval of relevant CI configurations and failure logs
* Autonomous risk analysis using LangGraph
* Automated pytest regression test generation
* Containerized deployment with Docker
* Kubernetes-based execution
* End-to-end performance benchmarking
* Separation of predictive ML and agentic AI layers

## 📈 Evaluation

The system evaluates both **predictive performance** and **execution architecture**:

* The ML classifier is evaluated using a held-out test split.
* Failure detection performance is measured using **Class 1 recall**.
* The agentic workflow is benchmarked through repeated graph executions.
* Kubernetes deployment is compared against direct execution to evaluate infrastructure overhead and end-to-end latency.

See [`RESULTS.md`](./RESULTS.md) for the detailed evaluation, results, and interview defense material.
