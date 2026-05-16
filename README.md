 # SentinelRAG — Agentic Compliance Intelligence Platform

## Overview

SentinelRAG is a production-grade Agentic AI compliance intelligence platform designed for sanctions screening, retrieval reasoning, explainable AI, and enterprise-scale decision workflows.

The platform combines:

* Hybrid Retrieval (Dense + BM25)
* Cross-Encoder Re-ranking
* Knowledge Graph Reasoning
* Risk-Aware Decision Intelligence
* Workflow Orchestration
* Human-in-the-loop Governance
* Active Learning Foundations
* Evaluation + Observability Pipelines
* Dockerized Deployment

Unlike traditional RAG systems, SentinelRAG focuses on explainability, governance, retrieval quality, and workflow orchestration required in real-world compliance and enterprise AI systems.

---

# Key Features

## Retrieval Intelligence

* Hybrid retrieval using semantic vector search + BM25
* Multi-signal ranking fusion
* Query expansion
* Metadata-aware retrieval
* Cross-encoder re-ranking
* Embedding benchmarking

## Agentic AI Workflow

* Multi-stage orchestration pipeline
* Retrieval reasoning traces
* Explainable decision generation
* Risk-aware classification
* Human review escalation
* Active learning candidate detection
* Feedback loop infrastructure

## Evaluation Framework

* Precision@K
* Recall@K
* Retrieval benchmarking
* Failure analysis
* Latency benchmarking

## Observability

* Structured logging
* Request tracing
* Workflow tracing
* Retrieval traces
* Latency monitoring

## Deployment

* Dockerized FastAPI backend
* Swagger API documentation
* Portable production deployment

---

# System Architecture

```text
User Query
    ↓
Graph Lookup Service
    ↓
Hybrid Retrieval Engine
(Dense Retrieval + BM25)
    ↓
Hybrid Score Fusion
    ↓
Cross-Encoder Re-ranking
    ↓
Decision Engine
    ├── Risk Scoring
    ├── Explainability
    ├── Human Review
    └── Active Learning
    ↓
Workflow Orchestrator
    ↓
Final Compliance Decision
```

---

# Agentic Workflow Pipeline

SentinelRAG follows a multi-stage agentic reasoning workflow:

```text
Retrieve Candidates
    ↓
Apply Hybrid Fusion
    ↓
Cross-Encoder Re-ranking
    ↓
Deterministic Validation
    ↓
Risk Analysis
    ↓
Human Review Check
    ↓
Workflow Orchestration
    ↓
Final Decision
```

This architecture enables:

* explainable AI decisions
* workflow-level reasoning
* compliance governance
* adaptive learning pipelines

---

# Retrieval Pipeline

## Hybrid Retrieval

SentinelRAG combines:

* Dense semantic retrieval using Sentence Transformers
* Sparse keyword retrieval using BM25

## Multi-Signal Ranking

Final ranking combines:

* semantic similarity
* BM25 retrieval scores
* reranker scores

## Query Expansion

Short/noisy queries are expanded semantically to improve recall.

Example:

```text
bank
→ financial institution banking corporation
```

## Metadata Filtering

Supports filtered retrieval for:

* sanctions programs
* entity categories
* contextual constraints

---

# Explainable AI + Risk Intelligence

The platform generates:

* reasoning traces
* retrieval traces
* workflow traces
* risk levels
* human review recommendations

Example risk levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

---

# Human-in-the-Loop Governance

Uncertain or high-risk decisions are escalated for manual review.

Review triggers include:

* low confidence scores
* terrorism-related sanctions
* ambiguous entity matches

This mirrors real-world enterprise compliance systems.

---

# Active Learning Foundations

The platform identifies:

* uncertain predictions
* low-confidence matches
* review-heavy cases

These can later be used for:

* RLHF pipelines
* continual learning
* retraining datasets
* annotation workflows

---

# Evaluation Framework

Current evaluation metrics include:

| Metric               | Purpose                            |
| -------------------- | ---------------------------------- |
| Accuracy             | Overall classification correctness |
| Precision            | Match correctness                  |
| Recall               | Missed sanctions detection         |
| Precision@1          | Retrieval quality                  |
| Recall@1             | Retrieval completeness             |
| Latency Benchmarking | Performance evaluation             |
| Failure Analysis     | Error inspection                   |

---

# Tech Stack

## Backend

* FastAPI
* Python
* Uvicorn

## Retrieval

* ChromaDB
* BM25
* Sentence Transformers
* Cross Encoders

## AI / NLP

* HuggingFace Transformers
* LangChain
* RapidFuzz

## Evaluation

* Scikit-learn
* Custom Retrieval Metrics

## Observability

* Structured Logging
* Workflow Tracing

## Deployment

* Docker

---

# API Endpoints

## Single Screening

```http
POST /screen
```

### Example Request

```json
{
  "query": "osama"
}
```

### Example Response

```json
{
  "trace_id": "8f31d6f9",
  "decision": "MATCH",
  "entity_number": "12345",
  "matched_name": "BIN LADIN, Usama bin Muhammad bin Awad",
  "confidence": 0.94,
  "risk_level": "CRITICAL",
  "requires_review": true,
  "reason": "High partial similarity detected.",
  "reasoning_trace": [
    "Performed graph lookup.",
    "Retrieved candidates using hybrid retrieval.",
    "Applied cross-encoder reranking.",
    "Final decision: MATCH."
  ]
}
```

---

# Deployment

## Build Docker Image

```bash
docker build -t sentinelrag .
```

## Run Container

```bash
docker run -p 8000:8000 sentinelrag
```

## Open Swagger Docs

```text
http://localhost:8000/docs
```

---

# Engineering Highlights

SentinelRAG demonstrates:

* AI Systems Engineering
* Retrieval Engineering
* Agentic Workflow Design
* Explainable AI
* Human-in-the-loop AI
* Evaluation Engineering
* Production Deployment
* Observability Infrastructure

---

# Future Improvements

* Qdrant migration
* Redis caching
* Cloud deployment
* Kubernetes orchestration
* Grafana dashboards
* Multi-agent collaboration
* Real-time streaming workflows
* Distributed retrieval infrastructure

---

# Repository Structure

```text
SentinelRAG/
│
├── services/
├── retrieval/
├── reranking/
├── graph/
├── decision/
├── middleware/
├── configs/
├── utils/
│
├── evaluation/
├── benchmarks/
├── frontend/
├── tests/
│
├── Dockerfile
├── api.py
├── requirements.txt
└── README.md
```

---

# Author

**Nishu Kumari Singh**

MS Data Science — Arizona State University

Applied AI | Retrieval Engineering | Agentic AI | LLM Systems
