"""
AI Research Report Agent — FastAPI application entry point.
Run:  python main.py   or   uvicorn main:app --reload
"""
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.logger import logger
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 %s v%s starting [%s]", settings.app_name, settings.app_version, settings.app_env)
    yield
    logger.info("🛑 %s shutting down", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "An autonomous AI research agent that searches the web, synthesizes findings, "
        "and generates structured markdown reports using LangGraph + Groq/OpenAI."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if not settings.is_production else [],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.exception_handler(Exception)
async def global_handler(request, exc):
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["Root"])
def root():
    return {
        "name":    settings.app_name,
        "version": settings.app_version,
        "docs":    "/docs",
        "health":  f"{settings.api_prefix}/health",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=not settings.is_production)
