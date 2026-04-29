from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    query : str
    search_results: List[Dict[str, Any]]
    summary : str 
    final_reports : str