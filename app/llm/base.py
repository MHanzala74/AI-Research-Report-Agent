"""
Abstract base class for all LLM providers.
"""
from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Every LLM provider must implement generate()."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Send prompt → return text response."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name for logging."""
        ...
