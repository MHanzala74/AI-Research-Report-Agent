"""Response schemas."""
from typing import List, Dict
from pydantic import BaseModel, Field


class Source(BaseModel):
    title: str
    url: str


class ReportResponse(BaseModel):
    report:  str          = Field(..., description="Full markdown research report")
    summary: str          = Field(..., description="Condensed summary used to build the report")
    sources: List[Source] = Field(default_factory=list, description="Web sources used")
    query:   str          = Field(..., description="Original research query")


class ErrorResponse(BaseModel):
    detail: str
    query:  str = ""
