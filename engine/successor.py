from engine.state import State
from engine.grid import Grid
from engine.rules import is_valid_transition
from engine.transitions import apply_joint_action, get_valid_moves
from engine.state_ops import update_visited_mask
from typing import Tuple


Actions = Tuple[str,str]

def get_successor(state: State, grid:Grid) -> list[tuple[State, Actions]]:
    successors = []

    prev_pos1 = state.prev_positions[0] if state.prev_positions is not None else None
    prev_pos2 = state.prev_positions[1] if state.prev_positions is not None else None

    valid_moves1 = get_valid_moves(state.positions[0], prev_pos1)
    valid_moves2 = get_valid_moves(state.positions[1], prev_pos2)
    
    for name1,m1 in valid_moves1:
        for name2,m2 in valid_moves2:
            joint_move = (m1, m2)
            action = (name1, name2)

            # 1) apply move
            new_positions = apply_joint_action(state.positions, joint_move)

            # 2) validate
            if not is_valid_transition(state.positions, new_positions, grid):
                continue

            # 3) update visited mask
            new_mask = update_visited_mask(new_positions, state.visited_mask, grid)

            # 4) create new state
            new_state = State(new_positions, new_mask, state.positions)

            successors.append((new_state, action))

    return successors
     
