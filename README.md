# ⚖️ Bumbiro — AI Constitutional Assistant

> ⚖️ Making the Zimbabwe Constitution accessible through AI

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange)
![LLM](https://img.shields.io/badge/LLM-RAG%20System-purple)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🚀 Overview

**Bumbiro** is a production-grade AI assistant designed to answer questions about the Zimbabwe Constitution.

It leverages Retrieval-Augmented Generation (RAG), evaluation pipelines, and AI safety guardrails to provide accurate, context-grounded constitutional answers.

Bumbiro was designed to make the Zimbabwe Constitution more accessible, understandable, and interactive through AI.

Legal and constitutional documents are often difficult to navigate, especially for non-legal users. This system bridges that gap by enabling users to ask natural language questions and receive grounded answers directly from constitutional text.

---

## ⚖️ What is Bumbiro?

Bumbiro is an AI-powered constitutional assistant that enables users to interact with the Zimbabwe Constitution through natural language.

Instead of manually searching through legal documents, users can ask questions such as:

* "How do I become a Zimbabwean citizen?"
* "What rights are protected under the Constitution?"
* "What does the Constitution say about freedom of expression?"

The system retrieves relevant constitutional provisions and generates grounded, explainable answers.

---

## 🎯 Motivation

The Zimbabwe Constitution is the supreme law of the country, yet accessing and understanding it remains a challenge for many.

Bumbiro was built to:

* simplify access to constitutional knowledge
* enable natural language interaction with legal text
* reduce reliance on manual document search
* demonstrate how AI can be applied to real-world civic and legal systems

This project goes beyond a generic chatbot by focusing on **trust, accuracy, and legal grounding**.

---

## 🧱 System Architecture

```text
User (Streamlit UI)
        ↓
FastAPI API Layer
        ↓
Bumbiro RAG Pipeline
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

The system is specifically optimized for constitutional question answering, ensuring responses are grounded in the Zimbabwe Constitution rather than general knowledge.

---

## 🔁 RAG Pipeline Flow

```text
Zimbabwe Constitution Documents
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

### 🔍 Constitutional Question Answering

* Semantic search over Zimbabwe Constitution documents
* Context-grounded answers based on constitutional text
* Handles natural language queries (e.g., "How do I become a citizen?")
* Reduces hallucinations by strictly using retrieved legal context

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
|   |   ├── source_formatter.py
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
git https://github.com/SimbaMunatsi/rag-production-system.git
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
  "query": "How can I become a Zimbabwean citizen?",
  "session_id": "user123"
}
```

---

## 📊 Example Response

```json
{
  "answer": "A person may become a Zimbabwean citizen by registration if they meet conditions such as lawful residence or marriage to a Zimbabwean citizen, as provided in the Constitution.",
  "sources": [
    "Zimbabwe Constitution — Chapter 3: Citizenship"
  ]
}
```

---

## 🧪 Evaluation Strategy

Bumbiro is tested like a production AI system:

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

Most AI legal assistants:

❌ generic chatbot with no legal grounding
❌ no evaluation
❌ no safety
❌ no structure

Bumbiro:

✔ domain-specific (constitutional AI assistant)
✔ grounded in real legal documents
✔ evaluation pipelines
✔ modular architecture
✔ API-first system
✔ designed for civic and legal accessibility

---

## 🔭 Future Improvements

* document upload from UI
* streaming responses in frontend
* enhanced hybrid retrieval (keyword + vector)
* multi-agent system integration
* Docker & cloud deployment

---

## 👤 Author

**Simbarashe Munatsi**

---

## ⭐ Final Note

Bumbiro reflects how modern AI systems are engineered — not just built.

It demonstrates the transition from:

> “using LLMs” → **engineering domain-specific AI systems with real-world impact**

---
