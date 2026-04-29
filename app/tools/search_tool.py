from dotenv import load_dotenv
from tavily import TavilyClient
import os
from app.logger import logging
from app.exception import MyException
import sys

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query: str, max_results: int = 5):
    try:
        logging.info(f"Tavily search started | Query: {query}")

        response = tavily.search(
            query=query,
            max_results=max_results,
            search_depth='advanced'
        )

        results = []

        for item in response.get("results", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("url"),
                "snippet": item.get("content")
            })

        logging.info(f"Tavily search completed | Results: {len(results)}")

        return results

    except Exception as e:
        logging.error("Error in search_web", exc_info=True)
        raise MyException(e, sys)