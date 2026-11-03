"""
Tavily web search tool.
Returns a list of {title, link, snippet} dicts.
"""
from tavily import TavilyClient
from app.core.config import settings
from app.utils.logger import logger
from app.utils.exception import AgentException

_client = TavilyClient(api_key=settings.tavily_api_key)


def search_web(query: str, max_results: int | None = None) -> list[dict]:
    n = max_results or settings.search_max_results
    logger.info("Tavily search | query=%s | max=%d", query, n)
    try:
        resp = _client.search(query=query, max_results=n, search_depth=settings.search_depth)
        results = [
            {"title": r.get("title", ""), "link": r.get("url", ""), "snippet": r.get("content", "")}
            for r in resp.get("results", [])
        ]
        logger.info("Tavily search done | results=%d", len(results))
        return results
    except Exception as e:
        raise AgentException(e)
