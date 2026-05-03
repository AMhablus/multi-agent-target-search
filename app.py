# app.py
import streamlit as st
import time
from engine.grid import Grid, State
from engine.goal import goal_test
from engine.successor import get_successors
from search.bfs import bfs
from search.astar import astar
from evaluation.heuristics import h_max_distance, h_mst
from evaluation.scenarios import small_scenario, medium_scenario, large_scenario
from evaluation.metrics import format_result

st.set_page_config(page_title="Multi-Agent Search Visualizer", layout="wide")
st.title("🤖 Multi-Agent Goal Coverage Visualizer")

# ──────────────── SIDEBAR CONTROLS ────────────────
st.sidebar.header("⚙️ Controls")
scenario_name = st.sidebar.selectbox("Scenario", ["Small", "Medium", "Large"])
algo_name = st.sidebar.selectbox("Algorithm", ["BFS", "A* (Max Dist)", "A* (MST)"])
speed = st.sidebar.slider("Animation Speed (sec/step)", 0.05, 0.8, 0.2)
run_btn = st.sidebar.button("🚀 Run & Animate")

# ──────────────── SCENARIO LOADER ────────────────
@st.cache_resource
def load_scenario(name: str):
    if name == "Small":   return small_scenario()
    if name == "Medium":  return medium_scenario()
    return large_scenario()

grid, initial_state = load_scenario(scenario_name)

# ──────────────── GRID RENDERER ────────────────
def render_grid(grid: Grid, state: State, path=None) -> str:
    width, height = grid.width, grid.height
    obstacles = grid.obstacles
    goals = set(grid.goals)
    goal_indices = grid.goal_indices

    visited = {g for g, i in goal_indices.items() if state.visited_mask & (1 << i)}
    agents = {pos: i+1 for i, pos in enumerate(state.positions)}
    path_cells = set()
    if path:
        for s in path: path_cells.update(s.positions)

    html = "<div style='display:inline-block; font-family:monospace; font-size:14px; line-height:1.2;'>"
    for y in reversed(range(height)):
        for x in range(width):
            pos = (x, y)
            content, bg, color = "·", "#f8f9fa", "#333"
            
            if pos in agents:
                content, bg, color = str(agents[pos]), "#4a90e2" if agents[pos]==1 else "#2ecc71", "white"
            elif pos in goals:
                content, bg = ("✓" if pos in visited else "●"), "#27ae60" if pos in visited else "#f1c40f"
            elif pos in obstacles:
                content, bg, color = "█", "#2c3e50", "#95a5a6"
            elif pos in path_cells:
                content, bg, color = "○", "#9b59b6", "white"
                
            html += f"<span style='display:inline-block;width:24px;height:24px;text-align:center;line-height:24px;background:{bg};color:{color};margin:1px;border-radius:3px;box-shadow:0 1px 2px rgba(0,0,0,0.2);'>{content}</span>"
        html += "<br>"
    html += "</div>"
    return html

# ──────────────── MAIN EXECUTION ────────────────
if run_btn:
    st.subheader(f"📊 Running `{algo_name}` on `{scenario_name}` Scenario...")
    
    algo_map = {"BFS": (bfs, None), "A* (Max Dist)": (astar, h_max_distance), "A* (MST)": (astar, h_mst)}
    algo_fn, heuristic_fn = algo_map[algo_name]
    
    goal_fn = lambda s: goal_test(s, grid)
    successor_fn = lambda s: get_successors(s, grid)
    h_fn = (lambda s: heuristic_fn(s, grid)) if heuristic_fn else None

    start = time.perf_counter()
    result = algo_fn(initial_state, goal_fn, successor_fn, h_fn) if h_fn else algo_fn(initial_state, goal_fn, successor_fn)
    result.runtime = time.perf_counter() - start

    metrics = format_result(result)

    # Metrics Dashboard
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Cost", metrics["cost"])
    c2.metric("🔍 Nodes Expanded", metrics["nodes_expanded"])
    c3.metric("⏱️ Time", f"{metrics['runtime']:.4f}s")
    c4.metric("📏 Path Length", metrics["path_length"])

    # Live Animation
    st.subheader("🗺️ Live Execution")
    grid_placeholder = st.empty()
    progress = st.progress(0)

    for i, state in enumerate(result.path):
        grid_placeholder.markdown(render_grid(grid, state, path=result.path[:i+1]), unsafe_allow_html=True)
        progress.progress((i + 1) / len(result.path))
        time.sleep(speed)

    grid_placeholder.markdown(render_grid(grid, result.path[-1], path=result.path), unsafe_allow_html=True)
    progress.progress(1.0)
    st.success("✅ Solution Completed Successfully!")