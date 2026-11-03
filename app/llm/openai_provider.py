"""
OpenAI LLM provider (gpt-4o-mini).
Fallback provider when Groq is unavailable.
"""
from langchain_openai import ChatOpenAI
from app.llm.base import BaseLLMProvider
from app.core.config import settings
from app.utils.logger import logger
from app.utils.exception import AgentException


class OpenAIProvider(BaseLLMProvider):
    name = "OpenAI (gpt-4o-mini)"

    def __init__(self):
        self._model = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key or None,
        )

    def generate(self, prompt: str) -> str:
        logger.info("LLM call → %s", self.name)
        try:
            response = self._model.invoke(prompt)
            logger.info("LLM response received ← %s", self.name)
            return response.content
        except Exception as e:
            raise AgentException(e)
