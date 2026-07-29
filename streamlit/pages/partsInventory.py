from pathlib import Path
import sys

import streamlit as st

from api import (
    APIError,
    add_part,
    delete_part,
    get_parts,
    get_parts_in_range,
    search_part,
)


st.title("Parts Inventory")
st.caption(
    "The HashMap handles exact lookup. "
    "The BinarySearchTree handles ordered traversal and ranges."
)


add_tab, search_tab, delete_tab, range_tab = st.tabs(
    [
        "Add",
        "Search",
        "Delete",
        "Range",
    ]
)


# ---------------------------------------------------------------------------
# Add a part
# ---------------------------------------------------------------------------

with add_tab:
    with st.form(
        "add_part_form",
        clear_on_submit=True,
    ):
        item_num = st.number_input(
            "Part number",
            min_value=0,
            step=1,
        )

        item = st.text_input("Part name")

        submitted = st.form_submit_button(
            "Add part"
        )

        if submitted:
            try:
                result = add_part(
                    int(item_num),
                    item,
                )

                st.success(
                    f"Added {result['item_num']}: "
                    f"{result['item']}"
                )

                st.rerun()

            except APIError as exc:
                st.error(str(exc))


# ---------------------------------------------------------------------------
# Search for a part
# ---------------------------------------------------------------------------

with search_tab:
    search_num = st.number_input(
        "Part number to search",
        min_value=0,
        step=1,
        key="search_part_number",
    )

    if st.button(
        "Search part",
        key="search_part_button",
    ):
        try:
            result = search_part(
                int(search_num)
            )

            st.success(
                f"{result['item_num']}: "
                f"{result['item']}"
            )

        except APIError as exc:
            st.error(str(exc))


# ---------------------------------------------------------------------------
# Delete a part
# ---------------------------------------------------------------------------

with delete_tab:
    delete_num = st.number_input(
        "Part number to delete",
        min_value=0,
        step=1,
        key="delete_part_number",
    )

    if st.button(
        "Delete part",
        key="delete_part_button",
    ):
        try:
            result = delete_part(
                int(delete_num)
            )

            st.success(
                f"Deleted {result['item_num']}: "
                f"{result['item']}"
            )

            st.rerun()

        except APIError as exc:
            st.error(str(exc))


# ---------------------------------------------------------------------------
# Find parts within a number range
# ---------------------------------------------------------------------------

with range_tab:
    minimum_num = st.number_input(
        "Minimum part number",
        min_value=0,
        step=1,
        key="minimum_part_number",
    )

    maximum_num = st.number_input(
        "Maximum part number",
        min_value=0,
        step=1,
        key="maximum_part_number",
    )

    if st.button(
        "Find range",
        key="find_range_button",
    ):
        try:
            result = get_parts_in_range(
                int(minimum_num),
                int(maximum_num),
            )

            if result["items"]:
                st.dataframe(
                    result["items"],
                    use_container_width=True,
                    hide_index=True,
                )

                st.caption(
                    f"Parts found: {result['count']}"
                )

            else:
                st.info(
                    "No parts were found in that range."
                )

        except APIError as exc:
            st.error(str(exc))


# ---------------------------------------------------------------------------
# Display inventory
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Inventory")

order = st.selectbox(
    "Display order",
    [
        "inorder",
        "preorder",
        "postorder",
        "hashmap",
        "showall",
    ],
)


try:
    inventory = get_parts(order)

    if inventory["items"]:
        st.dataframe(
            inventory["items"],
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            f"Total parts: {inventory['count']}"
        )

    else:
        st.info("No parts have been added.")

except APIError as exc:
    st.error(str(exc))
