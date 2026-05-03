# evaluation/runner.py
import time
from engine.grid import Grid
from engine.state import State
from search.core import solve
from evaluation.metrics import format_result



"""
    NOT USED RIGHT NOW
"""

def run_algorithm(strategy: str, initial_state: State, grid: Grid, scenario: str = "") -> dict:
    """
    Run a single strategy via solve() and return a formatted metrics dict.
    Catches exceptions so a failing run doesn't break comparison tables.
    """
    t0 = time.perf_counter()
    try:
        result  = solve(strategy, initial_state, grid)
        runtime = time.perf_counter() - t0
        metrics = format_result(result, strategy=strategy, scenario=scenario)
        metrics["runtime"] = round(runtime, 4)
        return metrics
    except Exception as e:
        return {
            "strategy": strategy,
            "scenario": scenario,
            "status":   "error",
            "error":    str(e),
            "cost":     None,
            "time":     None,
            "steps":    None,
            "runtime":  round(time.perf_counter() - t0, 4),
        }


def compare_algorithms(initial_state: State, grid: Grid,
                       strategies: list[str], scenario: str = "") -> list[dict]:
    """
    Run every strategy in `strategies` on the same scenario and return
    a list of metrics dicts (one per strategy).
    """
    return [run_algorithm(s, initial_state, grid, scenario=scenario)
            for s in strategies]