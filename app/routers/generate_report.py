from fastapi import APIRouter, HTTPException
from app.schemas.request import QueryRequest
from app.schemas.response import ReportResponse
from app.agents.graph import run_agent
from app.logger import logging
from app.exception import MyException

router = APIRouter()


@router.post("/generate-report", response_model=ReportResponse)
async def generate_report(request: QueryRequest):
    try:
        logging.info(f"API called | Query: {request.query}")

        result = run_agent(request.query)

        logging.info("Report generated successfully")

        return ReportResponse(report=result)

    except MyException as me:
        logging.error(f"MyException in API: {str(me)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Agent Error: {str(me)}"
        )

    except Exception as e:
        logging.error("Unexpected error in API", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )