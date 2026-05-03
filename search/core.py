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

        state_key = make_state_key(state)

        if state_key in visited:
            continue

        visited.add(state_key)

        # Goal: ALL goal cells covered by EITHER agent (any agent, any goal)
        if goal_test(state, grid):
            return get_solution(strategy, current_node, len(visited))

        successors = get_successor(state, grid)

        for next_state in successors:
            action = derive_joint_action(state.positions, next_state.positions)
            next_node = add_node(strategy, current_node, action, next_state)
            fringe.append(next_node)

    return None


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def make_state_key(state):
    """
    Hashable key = joint positions of both agents + goal coverage mask.
    Two nodes at the same positions but different coverage are distinct —
    this is essential when any agent can cover any goal cell.
    """
    positions_key = tuple(tuple(p) for p in state.positions)  # ((r1,c1),(r2,c2))
    return (positions_key, state.visited_mask)


def derive_joint_action(old_positions, new_positions):
    """
    Diff old vs new positions per agent → joint action tuple.
    e.g. agent1 goes right, agent2 goes up  →  ('R', 'U')
    """
    DELTA_TO_MOVE = {
        (-1,  0): 'U',
        ( 1,  0): 'D',
        ( 0, -1): 'L',
        ( 0,  1): 'R',
        ( 0,  0): 'S',  # agent waited this step
    }
    moves = []
    for (old_r, old_c), (new_r, new_c) in zip(old_positions, new_positions):
        delta = (new_r - old_r, new_c - old_c)
        moves.append(DELTA_TO_MOVE.get(delta, '?'))
    return tuple(moves)  # one symbol per agent → ('R', 'U')


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


