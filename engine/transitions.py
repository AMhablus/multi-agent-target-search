MOVES = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}

def apply_move(pos, move):
    # move a single agent
    return (pos[0] + move[0], pos[1] + move[1])

def apply_joint_action(positions, joint_move):
    # move multiple agents at once
    new_pos1 = apply_move(positions[0], joint_move[0])
    new_pos2 = apply_move(positions[1], joint_move[1])
    return (new_pos1, new_pos2)