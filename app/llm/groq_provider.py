from langchain_groq import ChatGroq
from dotenv import load_dotenv
from app.logger import logging
from app.exception import MyException
import sys

load_dotenv()

model = ChatGroq(model="llama-3.3-70b-versatile")


def generate_with_groq(prompt: str):
    try:
        logging.info("Groq LLM call started")

        response = model.invoke(prompt)

        logging.info("Groq response received successfully")

        return response.content

    except Exception as e:
        logging.error("Error in generate_with_groq", exc_info=True)
        raise MyException(e, sys)