# evaluation/runner.py
import time
from typing import Callable, Dict, List, Any
from engine.grid import Grid, State
from engine.goal import goal_test
from engine.successor import get_successor
from evaluation.metrics import format_result


def run_algorithm(
    name: str,
    algo_fn: Callable,
    initial_state: State,
    grid: Grid,
    heuristic: Callable = None
) -> dict:
    """
    Execute a search algorithm on a given scenario, measure performance,
    and return a formatted metrics dictionary.
    """
    start_time = time.perf_counter()

    # Bind grid to engine functions to match search algorithm signatures
    goal_fn = lambda s: goal_test(s, grid)
    successor_fn = lambda s: get_successor(s, grid)

    try:
        if heuristic:
            heuristic_fn = lambda s: heuristic(s, grid)
            result = algo_fn(initial_state, goal_fn, successor_fn, heuristic_fn)
        else:
            result = algo_fn(initial_state, goal_fn, successor_fn)

        # Attach accurate runtime to the SearchResult object
        result.runtime = time.perf_counter() - start_time

        # Format using the shared metrics module and return
        return format_result(result)

    except Exception as e:
        runtime = time.perf_counter() - start_time
        # Fallback structure to prevent breaking comparison tables
        return {
            "name": name,
            "status": "failed",
            "error": str(e),
            "runtime": runtime,
            "path": [],
            "cost": 0,
            "nodes_expanded": 0,
            "max_frontier_size": 0
        }


def compare_algorithms(
    algorithms: Dict[str, Any],
    initial_state: State,
    grid: Grid
) -> List[dict]:
    """
    Run multiple algorithms on the exact same scenario and return a list of result dicts.
    
    Expected `algorithms` dict format:
    {
        "BFS": bfs,
        "A* (Max)": {"fn": astar, "heuristic": h_max_distance},
        "A* (MST)": {"fn": astar, "heuristic": h_mst}
    }
    """
    results: List[dict] = []
    for name, config in algorithms.items():
        # Flexible config parsing
        if isinstance(config, dict):
            fn = config.get("fn")
            h = config.get("heuristic")
        else:
            fn = config
            h = None

        res = run_algorithm(name, fn, initial_state, grid, heuristic=h)
        results.append(res)
    return results