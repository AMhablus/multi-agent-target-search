from engine.state import State
from engine.grid import Grid
from search.core import solve


def split_agent_paths(solution):
    agent1 = []
    agent2 = []

    for a1, a2 in solution:
        agent1.append(a1)
        agent2.append(a2)

    return agent1, agent2

# Simple 5x5 maze:
# S = agent start, G = goal, # = wall
#
#  A . . . A
#  . # # . .
#  . . . # .
#  . . . . .
#  . . G . G   ← two goals at (4,2) and (4,4)
#
# Agent 1 starts at (0,0), Agent 2 starts at (0,4)

walls = {(1,1),(1,2),(2,3)}
goals = [(4,2), (4,4), (3,0)]   # index 0 → bit 0, index 1 → bit 1

grid = Grid(size=5, obstacles=walls, goals=goals)

# Initial state: no goals visited yet → mask = 0b00 = 0
initial_state = State(
    positions=((0,0), (0,4)),
    visited_mask=0
)

for strategy in ['BFS', 'DFS', 'A*']:
    result = solve(strategy, initial_state, grid)
    if result:
        print(f"\n{strategy} Solution found!")
        print(f"  Steps : {len(result['solution'])}")
        print(f"  Time  : {result['time']} states expanded")

        agent1, agent2 = split_agent_paths(result['solution'])

        print("  Agent 1:", " -> ".join(agent1))
        print("  Agent 2:", " -> ".join(agent2))