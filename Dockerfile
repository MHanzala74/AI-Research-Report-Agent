# ─────────────────────────────────────────────────────────────────────
#  AI Research Report Agent — Production Dockerfile
# ─────────────────────────────────────────────────────────────────────

FROM python:3.11-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim AS runtime
LABEL maintainer="MHanzala74"
LABEL description="AI Research Report Agent — LangGraph + Groq + Tavily"

RUN useradd --create-home agent
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app/       ./app/
COPY prompts/   ./prompts/
COPY main.py    .

RUN mkdir -p logs reports && chown -R agent:agent /app
USER agent

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')"

EXPOSE 8000
CMD ["python", "main.py"]
