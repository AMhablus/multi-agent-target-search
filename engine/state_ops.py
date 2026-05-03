from engine.grid import Grid

def update_visited_mask(positions, visited_mask, grid:Grid):
    new_mask = visited_mask
    for pos in positions:
        if grid.is_goal(pos):
            goal_idx = grid.goals_indeces[pos]
            new_mask = new_mask | (1 << goal_idx)
    return new_mask 