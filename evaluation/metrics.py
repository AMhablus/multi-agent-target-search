from typing import Any, Dict
from search.result import SearchResult


def format_result(result: Any) -> Dict[str, Any]:
    """
    Convert a SearchResult object (or error dict) into a standardized dictionary
    for logging, comparison tables, and JSON export.
    """
    # If it's already a dict (e.g., error/fallback from runner.py), return as-is
    if isinstance(result, dict):
        return result

    if not isinstance(result, SearchResult):
        raise TypeError(f"Expected SearchResult or dict, got {type(result).__name__}")

    return {
        "status": "success",
        "cost": result.cost,
        "nodes_expanded": result.nodes_expanded,
        "max_frontier_size": result.max_frontier_size,
        "runtime": round(result.runtime, 4),
        "path_length": len(result.path),
    }