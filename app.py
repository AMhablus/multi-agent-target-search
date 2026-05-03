# app.py
import streamlit as st
import time

from engine.grid import Grid
from engine.state import State
from engine.state_ops import update_visited_mask
from engine.transitions import apply_joint_action
from search.core import solve
from evaluation.scenarios import small_scenario, medium_scenario, large_scenario

# ──────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Multi-Agent Search Visualizer", layout="wide")
st.title("🤖 Multi-Agent Goal Coverage Visualizer")

# ──────────────────────────────────────────────────────────────────────
# Sidebar controls
# ──────────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Controls")
scenario_name = st.sidebar.selectbox("Scenario", ["Small", "Medium", "Large"])
algo_name     = st.sidebar.selectbox("Algorithm", ["BFS", "DFS", "A*"])
speed         = st.sidebar.slider("Animation Speed (sec/step)", 0.05, 1.0, 0.25)
run_btn       = st.sidebar.button("🚀 Run & Animate")

# ──────────────────────────────────────────────────────────────────────
# Scenario loader
# ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_scenario(name: str):
    if name == "Small":  return small_scenario()
    if name == "Medium": return medium_scenario()
    return large_scenario()

grid, initial_state = load_scenario(scenario_name)

# ──────────────────────────────────────────────────────────────────────
# Replay helper — reconstruct the sequence of States from the action list
# ──────────────────────────────────────────────────────────────────────
def replay_states(initial_state: State, solution: list, grid: Grid) -> list[State]:
    """
    Walk through the joint actions in `solution` and produce the full
    list of States visited, starting with the initial state.
    """
    states = [initial_state]
    current = initial_state
    for joint_move in solution:
        # joint_move is (name1, name2); we need the delta vectors
        from engine.transitions import MOVES
        m1 = MOVES[joint_move[0]]
        m2 = MOVES[joint_move[1]]
        new_positions = apply_joint_action(current.positions, (m1, m2))
        new_mask      = update_visited_mask(new_positions, current.visited_mask, grid)
        current       = State(new_positions, new_mask, prev_positions=current.positions)
        states.append(current)
    return states

# ──────────────────────────────────────────────────────────────────────
# Grid renderer — returns an HTML string
# ──────────────────────────────────────────────────────────────────────
def render_grid(grid: Grid, state: State, trail: set = None) -> str:
    size          = grid.size
    obstacles     = grid.obstacles
    goals_set     = set(grid.goals)
    goals_indeces = grid.goals_indeces

    visited_goals = {g for g, i in goals_indeces.items()
                     if state.visited_mask & (1 << i)}
    agents        = {pos: i + 1 for i, pos in enumerate(state.positions)}
    trail         = trail or set()

    cell  = "display:inline-block;width:28px;height:28px;text-align:center;" \
            "line-height:28px;margin:1px;border-radius:4px;" \
            "box-shadow:0 1px 3px rgba(0,0,0,.25);font-size:13px;"

    html = "<div style='display:inline-block;font-family:monospace;line-height:1;'>"
    for y in reversed(range(size)):
        for x in range(size):
            pos = (x, y)
            content, bg, color = "·", "#f0f2f5", "#555"

            if pos in agents:
                n = agents[pos]
                content = str(n)
                bg      = "#4a90e2" if n == 1 else "#2ecc71"
                color   = "white"
            elif pos in visited_goals:
                content, bg, color = "✓", "#27ae60", "white"
            elif pos in goals_set:
                content, bg, color = "●", "#f39c12", "white"
            elif pos in obstacles:
                content, bg, color = "█", "#2c3e50", "#95a5a6"
            elif pos in trail:
                content, bg, color = "·", "#d7bde2", "#555"

            html += f"<span style='{cell}background:{bg};color:{color};'>{content}</span>"
        html += "<br>"
    html += "</div>"
    return html

# ──────────────────────────────────────────────────────────────────────
# Run on button press
# ──────────────────────────────────────────────────────────────────────
if run_btn:
    st.subheader(f"📊 Running **{algo_name}** on **{scenario_name}** scenario…")

    strategy_map = {"BFS": "BFS", "DFS": "DFS", "A*": "A*"}
    strategy = strategy_map[algo_name]

    t0     = time.perf_counter()
    result = solve(strategy, initial_state, grid)
    runtime = time.perf_counter() - t0

    if result is None:
        st.error("❌ No solution found for this scenario.")
        st.stop()

    solution = result["solution"]   # list of (name1, name2) joint actions
    cost     = result["cost"]       # step count
    expanded = result["time"]       # nodes expanded

    # ── Metrics ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Cost (steps)", cost)
    c2.metric("🔍 Nodes Expanded", expanded)
    c3.metric("⏱️ Runtime", f"{runtime:.4f}s")
    c4.metric("📏 Solution Length", len(solution))

    # ── Rebuild state sequence ──
    states = replay_states(initial_state, solution, grid)

    # ── Live animation ──
    st.subheader("🗺️ Live Execution")
    grid_placeholder = st.empty()
    progress_bar     = st.progress(0)

    trail: set = set()
    for i, state in enumerate(states):
        trail.update(state.positions)
        grid_placeholder.markdown(
            render_grid(grid, state, trail=trail),
            unsafe_allow_html=True,
        )
        progress_bar.progress((i + 1) / len(states))
        time.sleep(speed)

    progress_bar.progress(1.0)
    st.success("✅ Solution found and animated successfully!")

    # ── Path breakdown ──
    with st.expander("📋 Step-by-step action log"):
        for i, (a1, a2) in enumerate(solution):
            st.text(f"Step {i+1:>3}: Agent1={a1:<6}  Agent2={a2}")