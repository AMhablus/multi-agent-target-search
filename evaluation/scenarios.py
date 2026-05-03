from engine.grid import Grid, State

Position = tuple[int, int]
GridSize = tuple[int, int]


def small_scenario() -> tuple[Grid, State]:
    """5x5 map, 2 agents, 3 goals, minimal obstacles."""
    size: GridSize = (5, 5)
    obstacles: set[Position] = {(2, 2)}
    goals: list[Position] = [(1, 1), (3, 3), (4, 0)]
    grid = Grid(size, obstacles, goals)

    initial_positions: tuple[Position, ...] = ((0, 0), (0, 4))
    initial_state = State(positions=initial_positions, visited_mask=0)
    return grid, initial_state


def medium_scenario() -> tuple[Grid, State]:
    """8x6 map, more obstacles, scattered goals."""
    size: GridSize = (8, 6)
    obstacles: set[Position] = {
        (2, 1), (2, 2), (3, 3), (4, 3), (5, 1), (5, 2)
    }
    goals: list[Position] = [(1, 4), (6, 0), (7, 5)]
    grid = Grid(size, obstacles, goals)

    initial_positions: tuple[Position, ...] = ((0, 0), (0, 5))
    initial_state = State(positions=initial_positions, visited_mask=0)
    return grid, initial_state


def large_scenario() -> tuple[Grid, State]:
    """10x10 map, dense obstacles, goals in corners."""
    size: GridSize = (10, 10)
    obstacles: set[Position] = {
        (i, 4) for i in range(1, 6)
    } | {(4, j) for j in range(1, 5)}
    goals: list[Position] = [(0, 9), (9, 0), (8, 8)]
    grid = Grid(size, obstacles, goals)

    initial_positions: tuple[Position, ...] = ((1, 1), (1, 8))
    initial_state = State(positions=initial_positions, visited_mask=0)
    return grid, initial_state