from app.llm.openai_provider import generate_with_openai
from app.llm.groq_provider import generate_with_groq
from app.logger import logging
from app.exception import MyException
import sys


def generate_text(prompt: str):
    try:
        logging.info("Trying Groq LLM...")
        return generate_with_groq(prompt)

    except Exception as e:
        logging.warning("Groq failed, switching to OpenAI...", exc_info=True)

        try:
            logging.info("Trying OpenAI LLM...")
            return generate_with_openai(prompt)

        except Exception as e2:
            logging.error("Both Groq and OpenAI failed", exc_info=True)
            raise MyException(e2, sys)