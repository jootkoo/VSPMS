from pathlib import Path
import sys


from datetime import date

import streamlit as st

from api import (
    APIError,
    add_repair_log,
    delete_repair_log,
    get_repair_logs,
    insert_repair_log,
)


st.title("Repair Logs")
st.caption(
    "FastAPI stores each log in your doubly linked list."
)

add_tab, insert_tab, delete_tab = st.tabs(
    ["Append", "Insert", "Delete"]
)

with add_tab:
    with st.form(
        "append_repair_log",
        clear_on_submit=True,
    ):
        repair_date = st.date_input(
            "Repair date",
            value=date.today(),
            key="append_date",
        )
        repair = st.text_area(
            "Repair performed",
            key="append_repair",
        )
        submitted = st.form_submit_button(
            "Append repair log"
        )

        if submitted:
            try:
                add_repair_log(
                    {
                        "month": repair_date.month,
                        "day": repair_date.day,
                        "year": repair_date.year,
                        "repair": repair,
                    }
                )
                st.success("Repair log added")
                st.rerun()
            except APIError as exc:
                st.error(str(exc))

with insert_tab:
    with st.form(
        "insert_repair_log",
        clear_on_submit=True,
    ):
        index = st.number_input(
            "Insert index",
            min_value=0,
            step=1,
        )
        repair_date = st.date_input(
            "Repair date",
            value=date.today(),
            key="insert_date",
        )
        repair = st.text_area(
            "Repair performed",
            key="insert_repair",
        )
        submitted = st.form_submit_button(
            "Insert repair log"
        )

        if submitted:
            try:
                insert_repair_log(
                    {
                        "index": int(index),
                        "month": repair_date.month,
                        "day": repair_date.day,
                        "year": repair_date.year,
                        "repair": repair,
                    }
                )
                st.success("Repair log inserted")
                st.rerun()
            except APIError as exc:
                st.error(str(exc))

with delete_tab:
    index = st.number_input(
        "Log index to delete",
        min_value=0,
        step=1,
        key="delete_log_index",
    )

    if st.button("Delete repair log"):
        try:
            delete_repair_log(int(index))
            st.success("Repair log deleted")
            st.rerun()
        except APIError as exc:
            st.error(str(exc))

try:
    logs = get_repair_logs()["logs"]
    rows = [
        {"index": index, **log}
        for index, log in enumerate(logs)
    ]

    if rows:
        st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No repair logs have been added")
except APIError as exc:
    st.error(str(exc))
