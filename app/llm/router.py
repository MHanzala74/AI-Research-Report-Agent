"""
LLM Router — tries Groq first, falls back to OpenAI.
Usage:  from app.llm.router import llm_router
        text = llm_router.generate(prompt)
"""
from app.llm.groq_provider import GroqProvider
from app.llm.openai_provider import OpenAIProvider
from app.utils.logger import logger
from app.utils.exception import AgentException


class LLMRouter:
    """Tries providers in order; raises AgentException if all fail."""

    def __init__(self):
        self._providers = [GroqProvider(), OpenAIProvider()]

    def generate(self, prompt: str) -> str:
        last_error = None
        for provider in self._providers:
            try:
                return provider.generate(prompt)
            except Exception as e:
                logger.warning("Provider %s failed: %s — trying next", provider.name, e)
                last_error = e

        raise AgentException(last_error or RuntimeError("All LLM providers failed"))


llm_router = LLMRouter()
