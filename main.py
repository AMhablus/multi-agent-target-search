from engine.state import State
from engine.grid import Grid
from engine.state_ops import update_visited_mask
from engine.transitions import apply_joint_action, MOVES
from search.core import solve
from evaluation.scenarios import small_scenario, medium_scenario, large_scenario
from evaluation.visualization import print_grid, animate_path
from evaluation.metrics import format_result, print_comparison_table
import time


# ──────────────────────────────────────────────────────────────────────────────
# Replay helper (mirrors the one in app.py)
# ──────────────────────────────────────────────────────────────────────────────

def replay_states(initial_state: State, solution: list, grid: Grid) -> list[State]:
    """Rebuild the full State sequence from the list of joint actions."""
    states = [initial_state]
    current = initial_state
    for joint_move in solution:
        m1 = MOVES[joint_move[0]]
        m2 = MOVES[joint_move[1]]
        new_positions = apply_joint_action(current.positions, (m1, m2))
        new_mask      = update_visited_mask(new_positions, current.visited_mask, grid)
        current       = State(new_positions, new_mask, prev_positions=current.positions)
        states.append(current)
    return states


# ──────────────────────────────────────────────────────────────────────────────
# Scenarios
# ──────────────────────────────────────────────────────────────────────────────

SCENARIOS = {
    "Small":  small_scenario,
    "Medium": medium_scenario,
    "Large":  large_scenario,
}

STRATEGIES = ["BFS", "DFS", "A*"]


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    # ── Let the user pick scenario & strategy ──
    print("\nAvailable scenarios:", ", ".join(SCENARIOS))
    scenario_name = input("Choose scenario [Small]: ").strip() or "Small"
    if scenario_name not in SCENARIOS:
        print(f"Unknown scenario '{scenario_name}', defaulting to Small.")
        scenario_name = "Small"

    print("\nAvailable strategies:", ", ".join(STRATEGIES))
    strategy = input("Choose strategy  [BFS]:  ").strip() or "BFS"
    if strategy not in STRATEGIES:
        print(f"Unknown strategy '{strategy}', defaulting to BFS.")
        strategy = "BFS"

    animate = input("\nAnimate solution? [y/N]: ").strip().lower() == "y"
    compare = input("Run all strategies for comparison? [y/N]: ").strip().lower() == "y"

    grid, initial_state = SCENARIOS[scenario_name]()

    # ── Show initial grid ──
    print(f"\n{'─'*40}")
    print(f"  Scenario : {scenario_name}  ({grid.size}×{grid.size})")
    print(f"  Strategy : {strategy}")
    print(f"  Goals    : {grid.goals}")
    print(f"  Agents   : {initial_state.positions}")
    print(f"{'─'*40}")
    print_grid(grid, state=initial_state)

    # ── Solve ──
    print(f"\nSolving with {strategy}…")
    t0     = time.perf_counter()
    result = solve(strategy, initial_state, grid)
    runtime = time.perf_counter() - t0

    if result is None:
        print("\n❌  No solution found.")
    else:
        solution = result["solution"]
        print(f"\n✅  Solution found!")
        print(f"   Steps expanded : {result['time']}")
        print(f"   Path length    : {len(solution)}")
        print(f"   Cost           : {result['cost']}")
        print(f"   Runtime        : {runtime:.4f}s")

        # ── Step-by-step path log ──
        print(f"\nAction log:")
        for i, (a1, a2) in enumerate(solution):
            print(f"  Step {i+1:>3}: Agent1={a1:<6}  Agent2={a2}")

        # ── Final grid snapshot ──
        states = replay_states(initial_state, solution, grid)
        print(f"\nFinal state:")
        print_grid(grid, state=states[-1], path=states)

        # ── Optional animation ──
        if animate:
            input("\nPress Enter to start animation…")
            animate_path(grid, states, delay=0.35)

    # ── Optional comparison table ──
    if compare:
        print("\nRunning all strategies for comparison…\n")
        rows = []
        for strat in STRATEGIES:
            r = solve(strat, initial_state, grid)
            rows.append(format_result(r, strategy=strat, scenario=scenario_name))
        print_comparison_table(rows)


if __name__ == "__main__":
    main()