# 📊 Empirical Results & Architectural Defense Documentation

This document records the empirical results, evaluation metrics, and system timing benchmarks for the **Agentic CI/CD Risk Simulation** system.

---

## Part A: LangGraph + RAG Autonomous Test Agent

### 1. Architecture Specification

* **Workflow Framework:** Directed 3-node `StateGraph` using `langgraph`
* **Graph Flow:** `retrieve_context` → `analyze_risk` → `generate_tests` → `END`
* **Vector Store Engine:** `ChromaDB` (persistent local vector store)
* **LLM Model:** `gemini-3.6-flash`

  * Temperature: `0.1`
  * Timeout: `30s`
* **Context Ingestion:** Metadata-tagged YAML configurations (`source: config`) and raw failure build logs (`source: log`)

### 2. Direct Execution Performance

| Trial       | Execution Time |
| ----------- | -------------: |
| Trial 1     |         84.12s |
| Trial 2     |         81.05s |
| Trial 3     |         82.66s |
| **Average** |     **82.61s** |

**Average Execution Time:** **82.61 seconds** across 3 full graph invocations.

### Latency Bottleneck Analysis

Each execution cycle includes:

1. A vector similarity query against ChromaDB
2. A synchronous external HTTPS request to Google's Gemini API for **Risk Analysis**
3. A second synchronous external HTTPS request to Google's Gemini API for **Test Code Synthesis**

The two external LLM calls represent the primary source of latency in the agentic workflow.

---

## Part B: GitHub Actions Pipeline Failure Predictor

### 1. Dataset & Feature Engineering

* **Data Source:** Live GitHub Actions REST API (`/repos/{owner}/{repo}/actions/runs`)
* **Target Label (`y`):**

  * `1` = failure
  * `0` = success
* **Engineered Features (`X`):**

  1. `duration_norm`: Standard Z-score normalized build duration
  2. `is_pr`: Binary indicator for `pull_request` event triggers

     * `1` = Pull Request
     * `0` = Direct Push
* **Data Split:** 80% Training Set / 20% Held-Out Test Set

The duration feature is normalized using:

$$
Z = \frac{x - \mu}{\sigma}
$$

### 2. Evaluation Metrics on Held-Out Test Set

```text
Classification Report:
              precision    recall  f1-score   support

           0       0.75      0.60      0.67        10
           1       0.50      0.67      0.57         6

    accuracy                           0.62        16
   macro avg       0.62      0.63      0.62        16
weighted avg       0.66      0.62      0.63        16
```

### 3. Metric Interpretation

| Metric        | Class 1 (Failure) |
| ------------- | ----------------: |
| **Recall**    |          **0.67** |
| **Precision** |          **0.50** |
| **F1-score**  |          **0.57** |

**Failure Class Recall (0.67):** The model correctly identified approximately **67% of actual pipeline failures** in the held-out test set.

For CI/CD risk management, recall is particularly important because failing to identify a genuinely risky pipeline can allow problematic changes to proceed through the pipeline.

**Failure Class Precision (0.50):** Of the pipelines predicted as failures, **50% were actual failures** in the held-out test set, indicating that the classifier also produces false-positive risk alerts.

> **Important:** These metrics are based on a relatively small held-out test set of **16 samples**, so they should be interpreted as an experimental benchmark rather than a production-level performance estimate.

---

## Part C: Kubernetes (Minikube) Cloud-Native Deployment

### 1. Infrastructure Architecture

* **Containerization:** Docker container based on `python:3.10-slim`
* **Orchestration:** Kubernetes `Deployment` with 1 replica
* **Secret Injection:** Active `GEMINI_API_KEY` injected into the container environment
* **Networking:** Kubernetes `Service` configured with `NodePort: 30007`
* **Application Port:** Flask API exposed on port `5000`
* **Cluster Environment:** Minikube control-plane node using the Docker driver

### 2. End-to-End Cluster Benchmark Results

Requests were routed through the active Minikube NodePort tunnel into the isolated running pod.

| Pod Run     | Execution Time |
| ----------- | -------------: |
| Run 1       |         87.24s |
| Run 2       |         72.35s |
| Run 3       |         38.92s |
| **Average** |     **66.17s** |

**Average Pod Execution Time:** **66.17 seconds** across 3 benchmark runs.

### 3. Architectural Verification

The following components were successfully verified:

* End-to-end HTTP `POST` JSON ingestion through the `/generate` endpoint
* ChromaDB vector retrieval operating inside the isolated container filesystem
* Live outbound HTTPS traffic from the Kubernetes pod to external Gemini API endpoints
* Successful execution of the LangGraph workflow inside the deployed pod

---

## 🎯 Summary Benchmark Table

| System Component           | Execution Model            | Average Latency / Performance Metric |
| -------------------------- | -------------------------- | -----------------------------------: |
| **Classifier Model**       | Logistic Regression        |                     **Recall: 0.67** |
|                            |                            |                  **Precision: 0.50** |
|                            |                            |                   **Accuracy: 0.62** |
| **Agent Direct Execution** | Local Bare-Metal Python    |                           **82.61s** |
| **Agent Pod Execution**    | Minikube Kubernetes Tunnel |                           **66.17s** |

---

## 📌 Key Findings

### Predictive Layer

The Logistic Regression classifier achieved:

* **0.67 recall** for pipeline failures
* **0.50 precision** for predicted failures
* **0.62 overall accuracy**

The results demonstrate the feasibility of using lightweight pipeline metadata to identify potentially risky CI/CD executions.

### Agentic Layer

The LangGraph + RAG workflow averaged **82.61 seconds** in direct execution across three full invocations.

The primary latency source is the pair of synchronous Gemini API calls used for risk analysis and test synthesis.

### Kubernetes Layer

The same workflow averaged **66.17 seconds** when executed through the Minikube deployment and NodePort tunnel.

This benchmark demonstrates successful containerized and orchestrated execution of the complete agent pipeline, including internal vector retrieval and external LLM communication.

---

## 🧪 Benchmark Notes

The reported latency values represent the measured end-to-end execution time of the experimental workflow under the tested environment.

Because the benchmark includes external LLM API calls, observed latency can vary based on network conditions, API response time, and model-side processing.

The results are therefore best treated as **empirical measurements of this experimental setup**, rather than generalized performance guarantees.
