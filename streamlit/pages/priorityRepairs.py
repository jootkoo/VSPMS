from pathlib import Path
import sys

import streamlit as st

from api import (
    APIError,
    add_priority_repair,
    get_priority_repairs,
    get_priority_services,
    peek_priority_repair,
    process_priority_repair,
)


st.title("Priority Repairs")
st.caption(
    "FastAPI stores repair requests in your MaxHeap."
)

try:
    services = get_priority_services()["services"]
except APIError as exc:
    st.error(str(exc))
    services = []

with st.form(
    "priority_repair_form",
    clear_on_submit=True,
):
    name = st.text_input("Customer name")
    vehicle = st.text_input("Vehicle")
    service = st.selectbox(
        "Service",
        services or ["oil change"],
    )
    is_drivable = st.checkbox(
        "Vehicle is drivable",
        value=True,
    )
    is_activeleak = st.checkbox(
        "Vehicle has an active leak"
    )
    submitted = st.form_submit_button(
        "Add repair request"
    )

    if submitted:
        try:
            result = add_priority_repair(
                {
                    "name": name,
                    "vehicle": vehicle,
                    "service": service,
                    "is_drivable": is_drivable,
                    "is_activeleak": is_activeleak,
                }
            )
            st.success(
                f"Request added with priority "
                f"{result['priority']}"
            )
            st.rerun()
        except APIError as exc:
            st.error(str(exc))

peek_column, process_column = st.columns(2)

if peek_column.button(
    "View highest priority",
    width="stretch",
):
    try:
        st.json(peek_priority_repair())
    except APIError as exc:
        st.error(str(exc))

if process_column.button(
    "Process highest priority",
    width="stretch",
):
    try:
        result = process_priority_repair()
        st.success(
            f"Processing {result['service']} "
            f"for {result['name']}"
        )
        st.rerun()
    except APIError as exc:
        st.error(str(exc))

try:
    repairs = get_priority_repairs()["repairs"]

    if repairs:
        st.dataframe(
            repairs,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info(
            "No priority repairs have been added"
        )
except APIError as exc:
    st.error(str(exc))
