from engine.state import State
from engine.grid import Grid
from engine.rules import is_valid_transition
from engine.transitions import apply_joint_action, MOVES


def get_successor(state: State, grid:Grid) -> list[State]:
    successors = []
    for m1 in MOVES:
        for m2 in MOVES:
            joint_move = (m1, m2)

            # 1) apply move
            new_positions = apply_joint_action(state.positions, joint_move)

            # 2) validate
            if not is_valid_transition(state.positions, new_positions, grid):
                continue

            # 4) create new state
            new_state = State(new_positions, new_mask)

            successors.append(new_state)

    return successors
     
