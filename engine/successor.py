from engine.state import State
from engine.grid import Grid
from engine.rules import is_valid_transition
from engine.transitions import apply_joint_action, MOVES
from engine.state_ops import update_visited_mask
from typing import Tuple


Actions = Tuple[str,str]

def get_successor(state: State, grid:Grid) -> list[tuple[State, Actions]]:
    successors = []
    for name1,m1 in MOVES.items():
        for name2,m2 in MOVES.items():
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
            new_state = State(new_positions, new_mask)

            successors.append((new_state, action))

    return successors
     
