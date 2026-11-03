"""Request schemas."""
from pydantic import BaseModel, Field, field_validator
from app.core.config import settings


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=settings.max_query_length,
        description="The research topic or question.",
        examples=["What are the latest advancements in quantum computing?"],
    )

    @field_validator("query")
    @classmethod
    def strip_query(cls, v: str) -> str:
        return v.strip()

    model_config = {"json_schema_extra": {"example": {"query": "Impact of LLMs on software engineering"}}}
