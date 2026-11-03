<div align="center">

# 🤖 AI Research Report Agent

### Autonomous Research Pipeline · LangGraph · Groq · Tavily

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.1-orange)](https://langchain-ai.github.io/langgraph)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> Send a research query → get a structured, cited, markdown report in seconds.
> Powered by a 3-node LangGraph pipeline with automatic LLM fallback.

</div>

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Pipeline Architecture](#-pipeline-architecture)
- [API Endpoints](#-api-endpoints)
- [Quick Start](#-quick-start)
- [Docker Deployment](#-docker-deployment)
- [Environment Variables](#-environment-variables)
- [Project Structure](#-project-structure)

---

## 🔍 Overview

The AI Research Report Agent automates the process of researching a topic and generating a professional report. Given a natural language query, it:

1. **Searches** the web using Tavily AI for recent, relevant sources
2. **Synthesizes** raw snippets into a clean summary via Groq (llama-3.3-70b)
3. **Writes** a structured markdown report with headings, analysis, and citations

### Key Features

| Feature | Details |
|---|---|
| 🔄 3-node pipeline | LangGraph DAG: Researcher → Synthesizer → Report Builder |
| 🤖 Multi-LLM | Groq (primary) → OpenAI (automatic fallback) |
| 🔍 AI Search | Tavily deep search with source tracking |
| 📝 Structured reports | Introduction, Key Findings, Analysis, Conclusion |
| ⚡ Fast | Groq inference: < 3s for a full report |
| 🐳 Docker-ready | Single `docker compose up --build` |

---

## 🏗️ Pipeline Architecture

```
Query Input
     │
     ▼
┌──────────────────────────────────────────────────┐
│              FastAPI Application                  │
│   POST /api/v1/research/generate                  │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│            LangGraph Pipeline                     │
│                                                   │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐ │
│  │  Researcher  │───▶│ Synthesizer  │───▶│  Report Builder  │ │
│  │             │    │             │    │                  │ │
│  │ Tavily web  │    │ LLM summary │    │ LLM full report  │ │
│  │ search      │    │ of snippets │    │ with structure   │ │
│  └─────────────┘    └──────────────┘    └──────────────────┘ │
└──────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│              LLM Router                           │
│   1. Groq (llama-3.3-70b) ← primary              │
│   2. OpenAI (gpt-4o-mini) ← automatic fallback   │
└──────────────────────────────────────────────────┘
                   │
                   ▼
        ReportResponse (JSON)
        ├── report   (full markdown)
        ├── summary  (condensed)
        ├── sources  (list of URLs)
        └── query    (original input)
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API info |
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/research/generate` | Generate research report |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc |

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/research/generate \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest advancements in multimodal AI models 2025"}'
```

### Example Response

```json
{
  "query": "Latest advancements in multimodal AI models 2025",
  "report": "## Introduction\n\nMultimodal AI...",
  "summary": "Recent research shows...",
  "sources": [
    {"title": "GPT-4V Technical Report", "url": "https://..."},
    {"title": "Gemini 1.5 Pro Overview", "url": "https://..."}
  ]
}
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- API keys: [Groq](https://console.groq.com) · [Tavily](https://app.tavily.com) · [OpenAI](https://platform.openai.com/api-keys) (optional fallback)

### 1. Clone & Install

```bash
git clone https://github.com/MHanzala74/AI-Research-Report-Agent.git
cd AI-Research-Report-Agent

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

make install
# or: pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env — add GROQ_API_KEY and TAVILY_API_KEY at minimum
```

### 3. Run

```bash
make dev          # auto-reload (development)
make run          # production
```

API live at **http://localhost:8000** · Docs at **http://localhost:8000/docs**

---

## 🐳 Docker Deployment

```bash
docker compose up --build          # Start
docker compose up -d --build       # Background
docker compose logs -f agent       # Logs
docker compose down                # Stop
```

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | ✅ | — | Groq API key (primary LLM) |
| `TAVILY_API_KEY` | ✅ | — | Tavily search API key |
| `OPENAI_API_KEY` | ⬜ | — | OpenAI key (fallback LLM) |
| `APP_ENV` | ⬜ | `development` | `development` or `production` |
| `GROQ_MODEL` | ⬜ | `llama-3.3-70b-versatile` | Groq model name |
| `OPENAI_MODEL` | ⬜ | `gpt-4o-mini` | OpenAI model name |
| `SEARCH_MAX_RESULTS` | ⬜ | `5` | Max Tavily results per query |
| `LOG_LEVEL` | ⬜ | `INFO` | `DEBUG / INFO / WARNING / ERROR` |

---

## 📁 Project Structure

```
AI-Research-Report-Agent/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py        # Router aggregator
│   │       ├── health.py          # GET /health
│   │       └── research.py        # POST /research/generate
│   ├── agents/
│   │   ├── graph.py               # LangGraph pipeline builder
│   │   ├── state.py               # Shared AgentState TypedDict
│   │   ├── researcher.py          # Node 1: Tavily web search
│   │   ├── synthesizer.py         # Node 2: LLM summarization
│   │   └── report_builder.py      # Node 3: LLM report generation
│   ├── core/
│   │   └── config.py              # Centralized settings (pydantic-settings)
│   ├── llm/
│   │   ├── base.py                # Abstract LLM provider interface
│   │   ├── groq_provider.py       # Groq implementation
│   │   ├── openai_provider.py     # OpenAI implementation
│   │   └── router.py              # Auto-fallback LLM router
│   ├── schemas/
│   │   ├── request.py             # QueryRequest (validated)
│   │   └── response.py            # ReportResponse + Source
│   ├── tools/
│   │   └── search_tool.py         # Tavily search wrapper
│   └── utils/
│       ├── logger.py              # Rotating file + console logger
│       └── exception.py           # AgentException with traceback detail
├── prompts/
│   ├── synthesizer.md             # Summarization prompt template
│   └── report_builder.md          # Report generation prompt template
├── logs/                          # Auto-created, gitignored
├── reports/                       # For future report persistence
├── main.py                        # FastAPI app entry point
├── Makefile                       # Dev commands
├── Dockerfile                     # Production container
├── docker-compose.yml             # Full stack deployment
├── requirements.txt               # Python dependencies
└── .env.example                   # Environment variable template
```

---

<div align="center">
Built with ❤️ using LangGraph · FastAPI · Groq · Tavily
</div>
