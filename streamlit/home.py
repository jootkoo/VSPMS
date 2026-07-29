import streamlit as st

from api import APIError, dashboard, health


st.set_page_config(
    page_title="VSPMS Hub",
    page_icon="🚘",
    layout="wide",
)

st.title("Vehicle Service and Parts Management System")


try:
    health()
    statistics = dashboard()
    st.success("FastAPI backend connected")
except APIError as exc:
    st.error(str(exc))
    statistics = {
        "appointments": 0,
        "parts": 0,
        "priority_repairs": 0,
        "repair_logs": 0,
    }

columns = st.columns(4)
columns[0].metric(
    "Appointments",
    statistics["appointments"],
)
columns[1].metric(
    "Parts",
    statistics["parts"],
)
columns[2].metric(
    "Priority repairs",
    statistics["priority_repairs"],
)
columns[3].metric(
    "Repair logs",
    statistics["repair_logs"],
)

st.divider()

pages = [
    (
        "Appointments",
        "Queue schedule with Stack undo and redo",
        "pages/appointments.py",
    ),
    (
        "Parts Inventory",
        "HashMap lookup and BST ordering",
        "pages/partsInventory.py",
    ),
    (
        "Priority Repairs",
        "MaxHeap prioritization",
        "pages/priorityRepairs.py",
    ),
    (
        "Repair Logs",
        "Doubly linked repair history",
        "pages/repairLogs.py",
    ),
    (
        "Repair Process",
        "Graph-backed workflows",
        "pages/repairProcess.py",
    ),
    (
        "RAG Manual Assistant",
        "Vehicle-manual question answering",
        "pages/RAG.py",
    ),
]

for start in range(0, len(pages), 3):
    page_columns = st.columns(3)

    for column, (title, description, path) in zip(
        page_columns,
        pages[start:start + 3],
    ):
        with column:
            with st.container(border=True):
                st.subheader(title)
                st.write(description)

                if st.button(
                    f"Open {title}",
                    key=path,
                    width="stretch",
                ):
                    st.switch_page(path)
