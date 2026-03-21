# 🧠 Production Agentic RAG System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange)
![LLM](https://img.shields.io/badge/LLM-RAG%20System-purple)
![Status](https://img.shields.io/badge/Status-Active-success)

A **production-style Retrieval-Augmented Generation (RAG) system** with a clean chat interface, evaluation pipelines, and AI safety guardrails.

---

## 🚀 Overview

This project demonstrates how modern AI systems are built in production environments.

It combines:

* Retrieval-Augmented Generation (RAG)
* modular backend architecture
* evaluation-driven development
* AI safety guardrails
* clean user interface

Unlike basic chatbot projects, this system focuses on:

> **reliability, observability, and production readiness**

---

## 🧱 System Architecture

```text
User (Streamlit UI)
        ↓
FastAPI API Layer
        ↓
RAG Pipeline
 ├── Input Guardrails
 ├── Retriever (Chroma Vector DB)
 ├── Context Builder
 ├── Prompt Builder
 ├── LLM Generator
 ├── Output Guardrails
 └── Memory Manager
        ↓
Answer + Sources
```

---

## 🔁 RAG Pipeline Flow

```text
Documents
   ↓
Loader → Cleaner → Chunker
   ↓
Embedding Service
   ↓
Vector Store (ChromaDB)
   ↓
User Query
   ↓
Query Embedding
   ↓
Similarity Search
   ↓
Top-K Chunks
   ↓
LLM Generation
   ↓
Final Answer
```

---

## ✨ Core Features

### 🔍 Retrieval-Augmented Generation

* Semantic search using vector embeddings
* Context-aware responses grounded in knowledge base
* Improved answer accuracy vs standard LLM prompts

---

### 🧠 Memory System

* Conversation memory for multi-turn interactions
* Session-based context handling

---

### 🛡️ AI Safety Guardrails

* Prompt injection detection
* Output validation
* Hallucination mitigation

---

### 📊 Evaluation Pipeline

Built using:

* **Ragas**
* **DeepEval**

Metrics tracked:

* Answer relevance
* Faithfulness
* Context precision
* Hallucination detection

---

### ⚙️ Production API (FastAPI)

Endpoints:

```text
POST /query
POST /query-stream
GET  /health
```

Supports:

* session-based queries
* structured responses (answer + sources)
* streaming output

---

### 💬 Streamlit Chat Interface

* ChatGPT-style UI
* Clean user experience
* Example prompts
* Source visibility toggle
* Session-based interaction

---

## 🗂️ Project Structure

```text
rag-production-system/
│
├── app/
│   ├── api/
│   │   └── main.py
|   |   ├── dependencies.py
│   │   ├── routes.py
│   │   └── schemas.py
|   |   
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── vector_store.py
│   │
│   ├── ingestion/
│   │   ├── document_loader.py
│   │   ├── document_cleaner.py
│   │   ├── chunker.py
│   │   ├── embedder.py
|   |   ├── vector_store_manager.py
│   │   └── pipeline.py
│   │
│   ├── retrieval/
│   │   ├── base_retriever.py
│   │   ├── context_compressor.py
│   │   └── retriever.py
|   |   ├── hybrid_retriever.py
│   │   ├── query_rewriter.py
│   │   └── reranker.py
│   │
│   ├── generation/
│   │   ├── base_generator.py
│   │   ├── prompt_builder.py
|   |   |__ source_formatter.py
│   │   └── generator.py
│   │
│   ├── memory/
│   │   ├── conversation_memory.py
│   │   └── base_memory.py
|   |   ├── episodic_memory.py
│   │   ├── semantic_memory.py
│   │   └── memory_manager.py
│   │
│   ├── guardrails/
│   │   ├── guardrail_manager.py
│   │   ├── guardrails.py
│   │   └── hallucination_check.py
|   |   ├── input_filter.py
│   │   ├── pii_filter.py
│   │   └── prompt_injection.py
│   │
│   ├── rag/
│       ├── pipeline.py
│       └── service.py
│
├── data/
│   ├── data/
│   └── embeddings/
│
├── eval/
│   ├── datasets/
│   ├── ragas_eval.py
│   └── deepeval_tests.py
│
├── tests/
│   ├── unit/
│   ├── integration/
|   ├── guardrails/
│   └── rag_eval/
│
├── scripts/
│   ├── ingest_data.py
│   └── run_all_evals.py
│
├── .env
├── .env_example
├── requirements.txt
├── README.md
└── streamlit_app.py

```

---

## ⚡ Getting Started

### 1. Clone the repo

```bash
git https://github.com/SimbaMunatsi/rag-production-system
cd rag-production-system
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure environment variables

Create `.env`:

```env
OPENAI_API_KEY=your_key
LANGSMITH_API_KEY=your_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=your_project
LANGSMITH_ENDPOINT=your_endpoint
CHROMA_DB_PATH=./data/embeddings
```

---

### 4. Start FastAPI backend

```bash
uvicorn app.api.main:app --reload
```

Swagger UI:

```
http://localhost:8000/docs
```

---

### 5. Start Streamlit frontend

```bash
streamlit run streamlit_app.py
```

App UI:

```
http://localhost:8501
```

---

## 💡 Example Request

```json
POST /query

{
  "query": "What is AI?",
  "session_id": "user123"
}
```

---

## 📊 Example Response

```json
{
  "answer": "AI is the ability of machines to imitate human intelligence",
  "sources": [
    "data/docs/AI Foundations: page 3"
  ]
}
```

---

## 🧪 Evaluation Strategy

The system is tested like software:

* unit tests (retrieval + pipeline)
* LLM evaluation (Ragas, DeepEval)
* guardrail validation tests

This ensures:

> consistent, reliable, and measurable AI performance

---

## 🔒 Security Design

Includes protection against:

* prompt injection attacks
* unsafe output generation
* hallucinated responses

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Streamlit
* LangChain 
* ChromaDB
* Ragas
* DeepEval
* LangSmith

---

## 📈 Why This Project Stands Out

Most AI projects:

❌ simple chatbot
❌ no evaluation
❌ no safety
❌ no structure

This project:

✔ production-style architecture
✔ evaluation pipelines
✔ modular design
✔ API-first system
✔ real-world engineering practices

---

## 🔭 Future Improvements

* document upload from UI
* streaming responses in frontend
* hybrid retrieval (keyword + vector)
* multi-agent system integration
* Docker & cloud deployment

---

## 👤 Author

**Simbarashe Munatsi**

---

## ⭐ Final Note

This project reflects how modern AI systems are engineered — not just built.

It demonstrates the transition from:

> “using LLMs” → **engineering AI systems**

---
