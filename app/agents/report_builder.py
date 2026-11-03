"""
Report Builder node — generates the final structured report.
"""
from pathlib import Path
from app.agents.state import AgentState
from app.llm.router import llm_router
from app.utils.logger import logger
from app.utils.exception import AgentException

_PROMPT_TEMPLATE = (Path(__file__).parent.parent.parent / "prompts" / "report_builder.md").read_text()


def report_builder_node(state: AgentState) -> AgentState:
    logger.info("▶ Report Builder node started")

    summary = state.get("summary", "")
    query   = state.get("query", "")

    if not summary:
        raise AgentException(ValueError("Summary is empty — cannot build report"))

    prompt = _PROMPT_TEMPLATE.format(query=query, summary=summary)
    report = llm_router.generate(prompt)

    if not report:
        raise AgentException(ValueError("LLM returned an empty report"))

    state["final_report"] = report
    logger.info("✔ Report Builder node done | report_len=%d", len(report))
    return state
