from pathlib import Path
import sys

import streamlit as st

from api import (
    APIError,
    get_repair_process,
    get_repair_services,
)


st.title("Repair Process")
st.caption(
    "FastAPI builds each repair workflow with your Graph."
)

try:
    services = get_repair_services()["services"]
except APIError as exc:
    st.error(str(exc))
    services = []

service = st.selectbox(
    "Service",
    services or ["oil change"],
)

if "repair_step_index" not in st.session_state:
    st.session_state.repair_step_index = 0

if "selected_repair_service" not in st.session_state:
    st.session_state.selected_repair_service = service

if service != st.session_state.selected_repair_service:
    st.session_state.selected_repair_service = service
    st.session_state.repair_step_index = 0

try:
    workflow = get_repair_process(service)
except APIError as exc:
    st.error(str(exc))
    st.stop()

steps = workflow["steps"]

st.metric(
    "Estimated total time",
    (
        f"{workflow['hours']} hr "
        f"{workflow['remaining_minutes']} min"
    ),
)

if not steps:
    st.info("No workflow steps are available")
    st.stop()

index = min(
    st.session_state.repair_step_index,
    len(steps) - 1,
)
current = steps[index]

st.progress(
    (index + 1) / len(steps),
    text=f"Step {index + 1} of {len(steps)}",
)

with st.container(border=True):
    st.subheader(current["step"])
    st.write(
        f"Estimated time: "
        f"**{current['minutes']} minutes**"
    )

previous_column, next_column = st.columns(2)

if previous_column.button(
    "Previous step",
    disabled=index == 0,
    use_container_width=True,
):
    st.session_state.repair_step_index -= 1
    st.rerun()

if next_column.button(
    "Mark complete / Next",
    disabled=index == len(steps) - 1,
    use_container_width=True,
):
    st.session_state.repair_step_index += 1
    st.rerun()

with st.expander("View complete workflow"):
    st.dataframe(
        steps,
        use_container_width=True,
        hide_index=True,
    )

with st.expander("Graph traversal"):
    st.write("Breadth-first search")
    st.write(workflow["bfs_order"])
    st.write("Depth-first search")
    st.write(workflow["dfs_order"])
