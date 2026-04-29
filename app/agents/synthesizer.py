from app.llm.router import generate_text
from app.agents.state import AgentState
from app.logger import logging
from app.exception import MyException
import sys


def synthesizer_node(state: AgentState) -> AgentState:
    try:
        logging.info("Synthesizer Node started")

        results = state['search_results']

        content = "\n".join([r["snippet"] for r in results])

        logging.info("Generating summary using LLM...")
        summary = generate_text(prompt := f"""
        Summarize the following information in a clear and concise way:

        {content}
        """)

        state["summary"] = summary

        logging.info("Summary generated successfully")

        return state

    except Exception as e:
        logging.error("Error in synthesizer_node", exc_info=True)
        raise MyException(e, sys)