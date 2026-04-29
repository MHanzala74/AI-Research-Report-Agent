from langgraph.graph import StateGraph

from app.agents.state import AgentState
from app.agents.researcher import researcher_node
from app.agents.synthesizer import synthesizer_node
from app.agents.report_builder import report_builder_node

from app.logger import logging
from app.exception import MyException
import sys


def build_graph():
    try:
        logging.info("Building LangGraph...")

        graph = StateGraph(AgentState)

        graph.add_node("researcher", researcher_node)
        graph.add_node("synthesizer", synthesizer_node)
        graph.add_node("report_builder", report_builder_node)

        graph.set_entry_point("researcher")

        graph.add_edge("researcher", "synthesizer")
        graph.add_edge("synthesizer", "report_builder")

        graph.set_finish_point("report_builder")

        logging.info("Graph built successfully")

        return graph.compile()

    except Exception as e:
        logging.error("Error while building graph", exc_info=True)
        raise MyException(e, sys)


def run_agent(query: str):
    try:
        logging.info(f"Agent started | Query: {query}")

        app = build_graph()

        state = {
            "query": query,
            "search_results": [],
            "summary": "",
            "final_reports": ""
        }

        result = app.invoke(state)

        logging.info("Agent execution completed successfully")

        return result.get("final_reports", "No report generated")

    except Exception as e:
        logging.error("Unexpected error in run_agent", exc_info=True)
        raise MyException(e, sys)