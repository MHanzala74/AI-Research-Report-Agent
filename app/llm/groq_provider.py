"""
Groq LLM provider (llama-3.3-70b-versatile).
Primary provider — fast and free-tier friendly.
"""
from langchain_groq import ChatGroq
from app.llm.base import BaseLLMProvider
from app.core.config import settings
from app.utils.logger import logger
from app.utils.exception import AgentException


class GroqProvider(BaseLLMProvider):
    name = "Groq (llama-3.3-70b)"

    def __init__(self):
        self._model = ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key or None,
        )

    def generate(self, prompt: str) -> str:
        logger.info("LLM call → %s", self.name)
        try:
            response = self._model.invoke(prompt)
            logger.info("LLM response received ← %s", self.name)
            return response.content
        except Exception as e:
            raise AgentException(e)
