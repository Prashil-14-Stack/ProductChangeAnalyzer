import streamlit as st
import os
from datetime import datetime

BUCKET_FOLDER = "bucket"


def show_history():

    from components.ui import page_title
    page_title(
        ":material/history: Comparison History",
        "View previous product comparison analyses."
    )

    # =====================================
    # CHECK REPOSITORY
    # =====================================

    if not os.path.exists(
        BUCKET_FOLDER
    ):

        st.warning(
            "No history available."
        )

        return

    analysis_runs = sorted(
        os.listdir(BUCKET_FOLDER),
        reverse=True
    )

    analysis_runs = [

        run

        for run in analysis_runs

        if os.path.isdir(
            os.path.join(
                BUCKET_FOLDER,
                run
            )
        )

    ]

    if len(
        analysis_runs
    ) == 0:

        st.info(
            "No analysis has been performed yet."
        )

        return

    # =====================================
    # TABLE HEADER
    # =====================================

    h1, h2, h3, h4, h5, h6 = st.columns(
        [3, 2, 2, 2, 1, 1]
    )

    h1.markdown("**Analysis ID**")
    h2.markdown("**User**")
    h3.markdown("**Date**")
    h4.markdown("**Status**")
    h5.markdown("**Files**")
    h6.markdown("**View**")

    st.divider()

    # =====================================
    # HISTORY
    # =====================================

    for run in analysis_runs:

        folder_path = os.path.join(
            BUCKET_FOLDER,
            run
        )

        created_time = datetime.fromtimestamp(
            os.path.getctime(
                folder_path
            )
        )

        files = os.listdir(
            folder_path
        )

        c1, c2, c3, c4, c5, c6 = st.columns(
            [3, 2, 2, 2, 1, 1]
        )

        with c1:

            st.write(
                run
            )

        with c2:

            st.write(
                st.session_state.username
            )

        with c3:

            st.write(

                created_time.strftime(
                    "%d-%b-%Y %H:%M"
                )

            )

        with c4:

            st.success(
                "Completed"
            )

        with c5:

            st.write(
                len(files)
            )

        with c6:

            if st.button(

                "📂",

                key=f"history_{run}"

            ):

                st.info(

                    f"Repository contains {len(files)} files."

                )

    st.divider()

    # =====================================
    # SUMMARY
    # =====================================

    st.metric(

        "Total Analyses",

        len(analysis_runs)

    )