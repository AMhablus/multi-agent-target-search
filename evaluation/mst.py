from typing import List

Position = tuple[int, int]

def _manhattan(a: Position, b: Position) -> int:
    """Helper: Calculate Manhattan distance between two positions."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def mst_cost(points: List[Position]) -> int:
    """
    Compute the Minimum Spanning Tree (MST) cost for a list of positions
    using Manhattan distance as edge weights.

    Implements Prim's algorithm (O(V^2)), which is optimal for small, dense 
    graphs typical in multi-agent pathfinding scenarios.

    Args:
        points: List of (x, y) coordinates that need to be connected.

    Returns:
        Total integer cost of the MST. Returns 0 if <= 1 point is provided.
    """
    if len(points) <= 1:
        return 0

    n = len(points)
    in_mst = [False] * n
    min_dist = [float('inf')] * n
    min_dist[0] = 0  # Start MST from the first point

    total_cost = 0

    for _ in range(n):
        # 1. Pick the unvisited node with the smallest distance to the current MST
        u = -1
        for v in range(n):
            if not in_mst[v] and (u == -1 or min_dist[v] < min_dist[u]):
                u = v

        # 2. Add it to the MST
        in_mst[u] = True
        total_cost += min_dist[u]

        # 3. Update distances to all unvisited neighbors
        for v in range(n):
            if not in_mst[v]:
                dist = _manhattan(points[u], points[v])
                if dist < min_dist[v]:
                    min_dist[v] = dist

    return int(total_cost)