from engine.state import State
from engine.grid import Grid
from search.core import solve

# Simple 5x5 maze:
# S = agent start, G = goal, # = wall
#
#  . . . . .
#  . # # . .
#  . . . # .
#  . . . . .
#  . . G . G   ← two goals at (4,2) and (4,4)
#
# Agent 1 starts at (0,0), Agent 2 starts at (0,4)

walls = {(1,1),(1,2),(2,3)}
goals = [(4,2), (4,4)]   # index 0 → bit 0, index 1 → bit 1

grid = Grid(size=5, obstacles=walls, goals=goals)

# Initial state: no goals visited yet → mask = 0b00 = 0
initial_state = State(
    positions=((0,0), (0,4)),
    visited_mask=0
)

for strategy in ['BFS', 'DFS']:
    result = solve(strategy, initial_state, grid)
    if result:
        print(f"\n{strategy} Solution found!")
        print(f"  Steps : {len(result['solution'])}")
        print(f"  Time  : {result['time']} states expanded")
        print(f"  Path  : {result['solution']}")
    else:
        print(f"\n{strategy}: No solution found.")