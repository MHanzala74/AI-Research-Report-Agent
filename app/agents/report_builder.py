from app.llm.router import generate_text
from app.agents.state import AgentState
from app.logger import logging
from app.exception import MyException
import sys


def report_builder_node(state: AgentState) -> AgentState:
    try:
        logging.info("Report Builder Node started")

        summary = state.get("summary", "")
        query = state.get("query", "")

        if not query:
            raise ValueError("Query is missing in state")

        prompt = f"""
        You are an expert research assistant.

        Create a professional, detailed, and well-structured report.

        Topic: {query}

        Summary:
        {summary}

        Instructions:
        - Write in clear academic style
        - Add headings
        - Expand key points with explanations
        - Keep it concise but informative

        Structure:
        1. Introduction
        2. Key Points (with headings)
        3. Conclusion
        """

        logging.info("Generating report using LLM...")
        report = generate_text(prompt)

        if not report:
            raise ValueError("Empty response from LLM")

        state["final_reports"] = report

        logging.info("Report generated successfully")

        return state

    except Exception as e:
        logging.error("Error in report_builder_node", exc_info=True)
        raise MyException(e, sys)