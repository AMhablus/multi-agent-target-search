from typing import Tuple
Position = Tuple[int,int]
Positions = Tuple[Position, ...]


class State:
    def __init__(self, positions: Positions, visited_mask: int, prev_positions = None):
        self.positions = positions
        self.visited_mask = visited_mask
        self.prev_positions = prev_positions

    def __eq__(self, other):
        return self.positions == other.positions and self.visited_mask == other.visited_mask

    def __hash__(self):
        return hash((self.positions, self.visited_mask, self.prev_positions))

    # used for printing the state; example > print(obj) or str(obj)
    def __str__(self):
        return f"Positions: {self.positions}, Visited Mask: {self.visited_mask}"

    # used for debugging; example > print(repr(obj)) or repr(obj)
    def __repr__(self):
        return f"State({self.positions}, {self.visited_mask})"
