from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.generate_report import router as generate_report_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(generate_report_router)

@app.get("/")
def health_check():
    return {"status": "ok"}