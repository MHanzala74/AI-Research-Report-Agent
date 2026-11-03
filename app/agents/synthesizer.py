"""
Synthesizer node — condenses raw search snippets into a clean summary.
"""
from pathlib import Path
from app.agents.state import AgentState
from app.llm.router import llm_router
from app.utils.logger import logger
from app.utils.exception import AgentException

_PROMPT_TEMPLATE = (Path(__file__).parent.parent.parent / "prompts" / "synthesizer.md").read_text()


def synthesizer_node(state: AgentState) -> AgentState:
    logger.info("▶ Synthesizer node started")

    results = state.get("search_results", [])
    if not results:
        raise AgentException(ValueError("No search results to synthesize"))

    content = "\n\n".join(
        f"[{r['title']}]\n{r['snippet']}" for r in results if r.get("snippet")
    )

    prompt = _PROMPT_TEMPLATE.format(content=content)
    summary = llm_router.generate(prompt)

    state["summary"] = summary
    logger.info("✔ Synthesizer node done | summary_len=%d", len(summary))
    return state
