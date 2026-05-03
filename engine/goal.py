from engine.state import State
from engine.grid import Grid
def goal_test(state: State, grid: Grid):
    return state.visited_mask == grid.all_goals_mask