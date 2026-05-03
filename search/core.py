from engine.successor import get_successor
from engine.goal import goal_test


def solve(strategy, initial_state, grid):
    fringe = []
    visited = set()

    initial_node = init_node(strategy, initial_state)
    fringe.append(initial_node)

    while fringe:
        current_node = fringe.pop(select_node(strategy, fringe))
        state = current_node['state']


        if state in visited:
            continue
        visited.add(state)


        # Goal: ALL goal cells covered by EITHER agent (any agent, any goal)
        if goal_test(state, grid):
            return get_solution(strategy, current_node, len(visited))

        for next_state, action in get_successor(state, grid):        
            next_node = add_node(strategy, current_node, action, next_state)
            fringe.append(next_node)

    return None

# ---------------------------------------------------------------------------
# Node helpers
# ---------------------------------------------------------------------------

def select_node(strategy, fringe):
    if strategy == 'DFS': return -1  # stack  — pop from back
    if strategy == 'BFS': return 0   # queue  — pop from front


def init_node(strategy, initial_state):
    return {
        'state': initial_state,
        'path':  [],
    }


def add_node(strategy, current_node, action, next_state):
    return {
        'state': next_state,
        'path':  current_node['path'] + [action],
    }


def get_solution(strategy, current_node, time):
    return {
        'solution': current_node['path'],  # [('R','U'), ('S','D'), ('L','R'), ...]
        'time':     time,
    }


