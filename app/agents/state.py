"""
LangGraph shared state — passed between all agent nodes.
"""
from typing import TypedDict, List, Dict, Any


class SearchResult(TypedDict):
    title: str
    link: str
    snippet: str


class AgentState(TypedDict):
    query: str
    search_results: List[SearchResult]
    summary: str
    final_report: str
    sources: List[Dict[str, str]]
