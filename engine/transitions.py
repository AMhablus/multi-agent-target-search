MOVES = [
    (0, 1), # up
    (0, -1), # down
    (1, 0), # right
    (-1, 0) # left
    (0, 0), # stay
]

def apply_move(pos, move):
    # move a single agent
    return (pos[0] + move[0], pos[1] + move[1])

def apply_joint_action(positions, joint_move):
    # move multiple agents at once
    new_pos1 = apply_move(positions[0], joint_move[0])
    new_pos2 = apply_move(positions[1], joint_move[1])
    return (new_pos1, new_pos2)