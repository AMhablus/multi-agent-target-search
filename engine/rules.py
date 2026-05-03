from engine.grid import Grid

def is_swap(old_pos, new_pos):
    return old_pos[0] == new_pos[1] and old_pos[1] == new_pos[0]

def is_collision(pos):
    return pos[0] == pos[1]

def is_valid_transition(old_pos, new_pos, grid: Grid):
    for pos in new_pos:
        if not grid.in_bounds(pos) or grid.is_obstacle(pos):
            return False

    if is_collision(new_pos):
        return False
    
    if is_swap(old_pos, new_pos):
        return False
    
    return True