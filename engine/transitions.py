MOVES = {
    "UP": (0, 1),
    "DOWN": (0, -1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

def apply_move(pos, move):
    # move a single agent
    return (pos[0] + move[0], pos[1] + move[1])

def apply_joint_action(positions, joint_move):
    # move multiple agents at once
    new_pos1 = apply_move(positions[0], joint_move[0])
    new_pos2 = apply_move(positions[1], joint_move[1])
    return (new_pos1, new_pos2)

def get_valid_moves(position:tuple[int,int], prev_position:tuple[int,int]) -> list[tuple[str, tuple[int,int]]]:
    valid_moves = []

    for name, move in MOVES.items():
        new_pos = (position[0] + move[0], position[1] + move[1])
        
        # no immediate backtracking
        if prev_position is not None and new_pos == prev_position:
            continue

        valid_moves.append((name, move))

    return valid_moves