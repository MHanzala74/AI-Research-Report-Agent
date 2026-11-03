"""
Researcher node — searches the web via Tavily and populates search_results.
"""
from app.agents.state import AgentState
from app.tools.search_tool import search_web
from app.utils.logger import logger
from app.utils.exception import AgentException


def researcher_node(state: AgentState) -> AgentState:
    logger.info("▶ Researcher node started")

    query = state.get("query", "").strip()
    if not query:
        raise AgentException(ValueError("Query is empty"))

    results = search_web(query)

    if not results:
        logger.warning("No search results found for: %s", query)

    state["search_results"] = results
    state["sources"] = [{"title": r["title"], "url": r["link"]} for r in results]

    logger.info("✔ Researcher node done | results=%d", len(results))
    return state
