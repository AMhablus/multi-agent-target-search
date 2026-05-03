class Grid:
    def __init__(self, size, obstacles, goals):
        self.size = size
        # set > O(1) for lookups, list > O(n) for lookups
        self.obstacles = set(obstacles)

        # list > maintain order
        self.goals = list(goals)

        # dict > O(1) for lookups
        self.goals_indeces = {goal: i for i, goal in enumerate(goals)} # >> {(0, 0): 0, (1, 1): 1....etc}
        self.all_goals_mask = (1 << len(goals)) - 1 # >> 1111....etc (binary)


    def in_bounds(self, pos):
        # tuple unpack > O(1)
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size    
    
    def is_obstacle(self, pos):
        return pos in self.obstacles

    def is_goal(self, pos):
        return pos in self.goals