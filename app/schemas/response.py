from pydantic import BaseModel

class ReportResponse(BaseModel):
    report: str
    
