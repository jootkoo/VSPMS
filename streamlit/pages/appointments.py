from pathlib import Path
import sys


import streamlit as st

from api import (
    APIError,
    add_appointment,
    get_appointments,
    process_appointment,
    redo_appointment,
    undo_appointment,
)


st.title("Appointments")
st.caption(
    "FastAPI uses Queue for the schedule and Stack for undo/redo."
)

with st.form(
    "add_appointment_form",
    clear_on_submit=True,
):
    appointment = st.text_input("Appointment")
    submitted = st.form_submit_button(
        "Add appointment"
    )

    if submitted:
        try:
            add_appointment(appointment)
            st.success("Appointment added")
            st.rerun()
        except APIError as exc:
            st.error(str(exc))

process_column, undo_column, redo_column = st.columns(3)

if process_column.button(
    "Process next",
    width="stretch",
):
    try:
        result = process_appointment()
        st.success(
            f"Processed: {result['processed']}"
        )
        st.rerun()
    except APIError as exc:
        st.error(str(exc))

if undo_column.button(
    "Undo",
    width="stretch",
):
    try:
        undo_appointment()
        st.success("Last action undone")
        st.rerun()
    except APIError as exc:
        st.error(str(exc))

if redo_column.button(
    "Redo",
    width="stretch",
):
    try:
        redo_appointment()
        st.success("Action redone")
        st.rerun()
    except APIError as exc:
        st.error(str(exc))

try:
    data = get_appointments()

    st.caption(
        f"Undo stack: {data['undo_count']} | "
        f"Redo stack: {data['redo_count']}"
    )

    rows = [
        {
            "position": index + 1,
            "appointment": appointment,
        }
        for index, appointment
        in enumerate(data["appointments"])
    ]

    if rows:
        st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("The appointment queue is empty")
except APIError as exc:
    st.error(str(exc))
