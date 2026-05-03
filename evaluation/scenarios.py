from engine.grid import Grid
from engine.state import State

Position = tuple[int, int]


def small_scenario() -> tuple[Grid, State]:
    """5x5 map, 2 agents, 3 goals, minimal obstacles."""
    grid = Grid(
        size=5,
        obstacles={(2, 2)},
        goals=[(1, 1), (3, 3), (4, 0)],
    )
    initial_state = State(positions=((0, 0), (0, 4)), visited_mask=0)
    return grid, initial_state


def medium_scenario() -> tuple[Grid, State]:
    """8x8 map, more obstacles, scattered goals."""
    grid = Grid(
        size=8,
        obstacles={(2, 1), (2, 2), (3, 3), (4, 3), (5, 1), (5, 2)},
        goals=[(1, 5), (6, 0), (7, 7)],
    )
    initial_state = State(positions=((0, 0), (0, 7)), visited_mask=0)
    return grid, initial_state


def large_scenario() -> tuple[Grid, State]:
    """10x10 map, dense obstacles, goals in corners."""
    grid = Grid(
        size=10,
        obstacles={(i, 4) for i in range(1, 6)} | {(4, j) for j in range(1, 5)},
        goals=[(0, 9), (9, 0), (8, 8)],
    )
    initial_state = State(positions=((1, 1), (1, 8)), visited_mask=0)
    return grid, initial_state