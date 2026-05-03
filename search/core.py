import heapq
from engine.successor import get_successor
from engine.goal import goal_test
from evaluation.heuristics import h_max_distance, h_mst


def solve(strategy, initial_state, grid):
    visited = set()


    initial_node = init_node(strategy, initial_state, grid)

    # A* uses a heap, BFS/DFS use a plain list
    if strategy == 'A*':
        fringe = []
        counter = 0   # tiebreaker when f values are equal
        heapq.heappush(fringe, (initial_node['f'], counter, initial_node))
    else:
        fringe = [initial_node]

    while fringe:
        if strategy == 'A*':
            _, _, current_node = heapq.heappop(fringe)
        else:
            current_node = fringe.pop(select_node(strategy))

        state = current_node['state']
    

        if state in visited:
            continue

        visited.add(state)
        

        if goal_test(state, grid):
            return get_solution(strategy, current_node, len(visited))

        for next_state, action in get_successor(state, grid):
            next_node = add_node(strategy, current_node, action, next_state, grid)

            if strategy == 'A*':
                counter += 1
                heapq.heappush(fringe, (next_node['f'], counter, next_node))
            else:
                fringe.append(next_node)

    return None


# ---------------------------------------------------------------------------
# Node helpers
# ---------------------------------------------------------------------------

def select_node(strategy):
    if strategy == 'DFS': return -1   # stack — pop from back
    if strategy == 'BFS': return 0    # queue — pop from front
    raise ValueError(f"Unknown strategy: {strategy}")


def init_node(strategy, initial_state, grid):
    h = h_mst(initial_state, grid) if strategy == 'A*' else 0
    return {
        'state': initial_state,
        'path':  [],
        'g':     0,        # steps taken so far
        'f':     0 + h,    # f = g + h
    }


def add_node(strategy, current_node, action, next_state, grid):
    g = current_node['g'] + 1
    h = h_mst(next_state, grid) if strategy == 'A*' else 0
    return {
        'state': next_state,
        'path':  current_node['path'] + [action],
        'g':     g,
        'f':     g + h,
    }


def get_solution(strategy, current_node, time):
    return {
        'solution': current_node['path'],
        'time':     time,
        'cost':     current_node['g'],   # exact step count
    }