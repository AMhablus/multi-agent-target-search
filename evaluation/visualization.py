# evaluation/visualization.py
from typing import List, Optional
from engine.grid import Grid
from engine.state import State

Position = tuple[int, int]
# ANSI color codes for terminal output (optional, gracefully degrades)
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    AGENT_1 = "\033[94m"  # Blue
    AGENT_2 = "\033[92m"  # Green
    GOAL = "\033[93m"     # Yellow
    VISITED = "\033[96m"  # Cyan
    OBSTACLE = "\033[90m" # Gray
    PATH = "\033[95m"     # Magenta


def print_grid(
    grid: Grid,
    state: Optional[State] = None,
    path: Optional[List[State]] = None,
    highlight_positions: Optional[List[Position]] = None
) -> None:
    """
    Print a human-readable representation of the grid with optional overlays.
    
    Args:
        grid: The Grid object containing size, obstacles, and goals.
        state: Current state to show agent positions and visited goals.
        path: List of states to highlight the solution path.
        highlight_positions: Extra positions to mark (e.g., for debugging).
    """
    size         = grid.size
    obstacles    = grid.obstacles
    goals        = set(grid.goals)
    goal_indices = grid.goals_indeces   # {(x,y): bit_index}
    
    # Track visited goals from state or path
    visited_goals: set[Position] = set()
    if state:
        for goal, idx in goal_indices.items():
            if state.visited_mask & (1 << idx):
                visited_goals.add(goal)
    if path and path[-1]:
        final_state = path[-1]
        for goal, idx in goal_indices.items():
            if final_state.visited_mask & (1 << idx):
                visited_goals.add(goal)
    
    # Agent positions from current state or last path state
    agent_positions: dict[Position, int] = {}
    if state:
        for i, pos in enumerate(state.positions):
            agent_positions[pos] = i
    elif path and path[-1]:
        for i, pos in enumerate(path[-1].positions):
            agent_positions[pos] = i
    
    # Path positions (all intermediate cells)
    path_cells: set[Position] = set()
    if path and len(path) > 1:
        for s1, s2 in zip(path, path[1:]):
            for (x1, y1), (x2, y2) in zip(s1.positions, s2.positions):
                # Simple linear interpolation for visualization
                dx, dy = x2 - x1, y2 - y1
                steps = max(abs(dx), abs(dy))
                if steps > 0:
                    for t in range(steps + 1):
                        path_cells.add((x1 + dx * t // steps, y1 + dy * t // steps))
    
    # Extra highlights
    highlights = set(highlight_positions) if highlight_positions else set()
    
    # Print top border
    print("  " + "─" * (size * 2 + 1))
    
    for y in reversed(range(size)):
        row = f"{y:2d} │"
        for x in range(size):
            pos = (x, y)
            char = "·"  # Default empty cell
            
            # Layer priority: agent > goal status > obstacle > path > highlight > empty
            if pos in agent_positions:
                agent_id = agent_positions[pos]
                char = f"{agent_id + 1}"  # Show agent number (1, 2, ...)
                color = Colors.AGENT_1 if agent_id == 0 else Colors.AGENT_2
                row += f" {color}{Colors.BOLD}{char}{Colors.RESET}"
            elif pos in goals:
                if pos in visited_goals:
                    char = "✓"
                    color = Colors.VISITED
                else:
                    char = "●"
                    color = Colors.GOAL
                row += f" {color}{char}{Colors.RESET}"
            elif pos in obstacles:
                char = "█"
                row += f" {Colors.OBSTACLE}{char}{Colors.RESET}"
            elif pos in path_cells:
                char = "○"
                row += f" {Colors.PATH}{char}{Colors.RESET}"
            elif pos in highlights:
                char = "★"
                row += f" {Colors.BOLD}{char}{Colors.RESET}"
            else:
                row += " ·"
        row += " │"
        print(row)
    
    # Print bottom border + x-axis labels
    print("  " + "─" * (size * 2 + 1))
    print("    " + " ".join(f"{x:1d}" for x in range(size)))
    
    # Legend
    print(f"\n{Colors.BOLD}Legend:{Colors.RESET}")
    print(f"  {Colors.AGENT_1}1{Colors.RESET} / {Colors.AGENT_2}2{Colors.RESET} = Agents  |  "
          f"{Colors.GOAL}●{Colors.RESET} = Goal  |  {Colors.VISITED}✓{Colors.RESET} = Visited  |  "
          f"{Colors.OBSTACLE}█{Colors.RESET} = Obstacle  |  {Colors.PATH}○{Colors.RESET} = Path")


def animate_path(
    grid: Grid,
    path: List[State],
    delay: float = 0.3,
    clear_screen: bool = True
) -> None:
    """
    Animate the solution path step-by-step in the terminal.
    
    Args:
        grid: The Grid object for map context.
        path: List of states representing the solution.
        delay: Seconds to wait between frames (default: 0.3).
        clear_screen: Whether to clear terminal between frames (requires 'os' module).
    """
    import time
    import os
    
    for i, state in enumerate(path):
        if clear_screen:
            os.system("cls" if os.name == "nt" else "clear")
        print(f"\n{Colors.BOLD}Step {i} / {len(path) - 1}{Colors.RESET}\n")
        print_grid(grid, state=state, path=path[:i+1])
        time.sleep(delay)
    
    # Final frame with summary
    if clear_screen:
        os.system("cls" if os.name == "nt" else "clear")
    print(f"\n{Colors.BOLD}✓ Solution Complete{Colors.RESET}\n")
    print_grid(grid, state=path[-1], path=path)
    print(f"\n{Colors.BOLD}Total Cost:{Colors.RESET} {len(path) - 1 if path else 'N/A'}")
    print(f"\n{Colors.BOLD}Total Steps:{Colors.RESET} {len(path) - 1}")