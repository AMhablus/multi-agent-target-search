class SearchResult:
     def __init__( self, path: list[State], cost: int, nodes_expanded: int, max_frontier_size: int, runtime: float ): 
        self.path = path
        self.cost = cost
        self.nodes_expanded = nodes_expanded
        self.max_frontier_size = max_frontier_size
        self.runtime = runtime