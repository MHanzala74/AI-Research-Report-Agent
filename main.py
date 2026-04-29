from fastapi import FastAPI
from app.routers.generate_report import router as generate_report_router

app = FastAPI()

app.include_router(generate_report_router)

