"""
LangGraph pipeline: researcher → synthesizer → report_builder
"""
from langgraph.graph import StateGraph
from app.agents.state import AgentState
from app.agents.researcher import researcher_node
from app.agents.synthesizer import synthesizer_node
from app.agents.report_builder import report_builder_node
from app.utils.logger import logger
from app.utils.exception import AgentException


def build_graph():
    logger.info("Building LangGraph pipeline...")
    try:
        g = StateGraph(AgentState)
        g.add_node("researcher",    researcher_node)
        g.add_node("synthesizer",   synthesizer_node)
        g.add_node("report_builder", report_builder_node)
        g.set_entry_point("researcher")
        g.add_edge("researcher",    "synthesizer")
        g.add_edge("synthesizer",   "report_builder")
        g.set_finish_point("report_builder")
        logger.info("Pipeline built ✔")
        return g.compile()
    except Exception as e:
        raise AgentException(e)


def run_agent(query: str) -> dict:
    """
    Run the full pipeline for a given query.

    Returns:
        dict with keys: final_report, sources, summary
    """
    logger.info("Agent run started | query=%s", query)
    try:
        pipeline = build_graph()
        state = {
            "query": query,
            "search_results": [],
            "summary": "",
            "final_report": "",
            "sources": [],
        }
        result = pipeline.invoke(state)
        logger.info("Agent run completed ✔")
        return {
            "final_report": result.get("final_report", ""),
            "summary":      result.get("summary", ""),
            "sources":      result.get("sources", []),
        }
    except Exception as e:
        raise AgentException(e)
