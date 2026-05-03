from typing import List
from engine.grid import Grid
from engine.state import State
from evaluation.mst import mst_cost


Position = tuple[int, int]


def manhattan(a: Position, b: Position) -> int:
    """Calculate Manhattan distance between two positions."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def remaining_goals(state: State, grid: Grid) -> List[Position]:
    """Return list of goal positions that have not been visited yet."""
    unvisited = []
    for goal in grid.goals:
        idx = grid.goals_indeces[goal]
        # Check if the bit corresponding to this goal is NOT set
        if not (state.visited_mask & (1 << idx)):
            unvisited.append(goal)
    return unvisited


def h_max_distance(state: State, grid: Grid) -> int:
    """Heuristic: Max Manhattan distance from any agent to any unvisited goal."""
    unvisited = remaining_goals(state, grid)
    if not unvisited:
        return 0

    max_dist = 0
    for agent_pos in state.positions:
        for goal_pos in unvisited:
            dist = manhattan(agent_pos, goal_pos)
            if dist > max_dist:
                max_dist = dist
    return max_dist


def h_mst(state: State, grid: Grid) -> int:
    """Heuristic: MST cost connecting all agents and remaining goals."""

    unvisited = remaining_goals(state, grid)
    if not unvisited:
        return 0

    # Combine current agent locations with unvisited goals
    points= list(state.positions) + unvisited

    if len(points) <= 1:
        return 0

    return mst_cost(points)