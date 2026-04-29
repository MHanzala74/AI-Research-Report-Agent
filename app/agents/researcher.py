from app.tools.search_tool import search_web
from .state import AgentState
from app.logger import logging
from app.exception import MyException
import sys


def researcher_node(state: AgentState) -> AgentState:
    try:
        logging.info("Researcher Node started")

        query = state.get("query", "")

        if not query:
            raise ValueError("Query is missing in state")

        logging.info(f"Searching web for query: {query}")

        results = search_web(query)

        if not results:
            logging.warning("No search results found")

        state["search_results"] = results

        logging.info("Search completed successfully")

        return state

    except Exception as e:
        logging.error("Error in researcher_node", exc_info=True)
        raise MyException(e, sys)
    
