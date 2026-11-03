"""
Research report generation endpoint.
POST /api/v1/research/generate
"""
from fastapi import APIRouter, HTTPException
from app.schemas.request import QueryRequest
from app.schemas.response import ReportResponse, ErrorResponse
from app.agents.graph import run_agent
from app.utils.logger import logger

router = APIRouter(prefix="/research", tags=["Research"])


@router.post(
    "/generate",
    response_model=ReportResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Generate an AI research report",
    description=(
        "Runs a 3-stage LangGraph pipeline:\n\n"
        "1. **Researcher** — searches the web via Tavily\n"
        "2. **Synthesizer** — condenses results into a summary\n"
        "3. **Report Builder** — produces a structured markdown report"
    ),
)
async def generate_report(request: QueryRequest):
    logger.info("POST /research/generate | query=%s", request.query)
    try:
        result = run_agent(request.query)
        return ReportResponse(
            report=result["final_report"],
            summary=result["summary"],
            sources=result["sources"],
            query=request.query,
        )
    except Exception as e:
        logger.error("Report generation failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
