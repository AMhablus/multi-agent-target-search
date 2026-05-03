from typing import Any, Dict


def format_result(result: Any, strategy: str = "", scenario: str = "") -> Dict[str, Any]:
    """
    Convert the dict returned by search.core.solve() into a standardised
    metrics dictionary ready for display or comparison tables.
    """
    if result is None:
        return {
            "strategy":  strategy,
            "scenario":  scenario,
            "status":    "no_solution",
            "cost":      None,
            "time":      None,
            "steps":     None,
        }

    return {
        "strategy": strategy,
        "scenario": scenario,
        "status":   "success",
        "cost":     result.get("cost"),        # exact step count (g-value)
        "time":     result.get("time"),        # nodes expanded
        "steps":    len(result.get("solution", [])),
    }


def print_comparison_table(rows: list[Dict]) -> None:
    """Print a formatted comparison table from a list of format_result() dicts."""
    header = f"{'Strategy':<8} {'Scenario':<10} {'Status':<12} {'Steps':>6} {'Cost':>6} {'Expanded':>10}"
    print("\n" + "=" * len(header))
    print(header)
    print("-" * len(header))
    for r in rows:
        steps    = r["steps"]    if r["steps"]    is not None else "—"
        cost     = r["cost"]     if r["cost"]     is not None else "—"
        expanded = r["time"]     if r["time"]     is not None else "—"
        print(f"{r['strategy']:<8} {r['scenario']:<10} {r['status']:<12} {str(steps):>6} {str(cost):>6} {str(expanded):>10}")
    print("=" * len(header) + "\n")