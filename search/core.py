from engine import get_successor
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

        if goal_test(state,grid):
            return get_solution(strategy, current_node, len(visited))

        successors = get_successor(state, grid)

        for action, next_state in successors:
            next_node = add_node(strategy, current_node, action, next_state)
            fringe.append(next_node)

    return None

def select_node(strategy,fringe):
	if strategy == 'DFS': return -1
	if strategy == 'BFS': return 0
	



def init_node(strategy,intial_state):
	initial_node = {}
	initial_node['state']=intial_state
	initial_node['path']=[]
	return initial_node

def add_node(strategy, current_node, action, next_state):
    next_node = {}

    next_node['state'] = next_state

    next_node['path'] = current_node['path'][:]
    next_node['path'].append(action)



    return next_node

def get_solution(strategy,current_node,time):
	solution={}
	solution['solution']=current_node['path']
	solution['time']=time
	return solution


