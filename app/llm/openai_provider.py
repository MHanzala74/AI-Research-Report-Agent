from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from app.logger import logging
from app.exception import MyException
import sys

load_dotenv()

model = ChatOpenAI(model="gpt-4o")


def generate_with_openai(prompt: str):
    try:
        logging.info("OpenAI LLM call started")

        response = model.invoke(prompt)

        logging.info("OpenAI response received successfully")

        return response.content

    except Exception as e:
        logging.error("Error in generate_with_openai", exc_info=True)
        raise MyException(e, sys)
