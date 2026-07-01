import streamlit as st
import os
from datetime import datetime


from config.repository_config import BUCKET_FOLDER


def show_repository():
    from components.ui import page_title
    page_title(
        ":material/folder: Document Repository",
        "Browse previous analysis runs and download associated documents."
    )

    # =====================================
    # NO ANALYSIS AVAILABLE
    # =====================================

    if not os.path.exists(BUCKET_FOLDER):

        st.warning(
            "Repository folder does not exist."
        )

        return

    analysis_runs = sorted(
        os.listdir(BUCKET_FOLDER),
        reverse=True
    )

    if len(analysis_runs) == 0:

        st.info(
            "No analysis available."
        )

        return

    # =====================================
    # LOOP THROUGH ANALYSIS
    # =====================================

    for run in analysis_runs:

        run_path = os.path.join(
            BUCKET_FOLDER,
            run
        )

        if not os.path.isdir(run_path):

            continue

        run_time = datetime.fromtimestamp(
            os.path.getctime(run_path)
        )

        with st.expander(
            f"📁 {run}",
            expanded=False
        ):

            # ============================
            # INFORMATION
            # ============================

            info1, info2, info3 = st.columns(3)

            with info1:

                st.write(
                    f"**User:** {st.session_state.username}"
                )

            with info2:

                st.write(
                    f"**Date:** {run_time.strftime('%d-%b-%Y %H:%M')}"
                )

            with info3:

                st.success(
                    "Completed"
                )

            st.divider()

            # ============================
            # FILES
            # ============================

            files = sorted(
                os.listdir(run_path)
            )

            if len(files) == 0:

                st.info(
                    "No files found."
                )

            else:

                header1, header2, header3 = st.columns(
                    [5, 2, 1]
                )

                header1.markdown("**Document**")
                header2.markdown("**Type**")
                header3.markdown("**Download**")

                st.divider()

                for file_name in files:

                    file_path = os.path.join(
                        run_path,
                        file_name
                    )

                    col1, col2, col3 = st.columns(
                        [5, 2, 1]
                    )

                    with col1:

                        st.write(
                            file_name
                        )

                    with col2:

                        if file_name.endswith(".docx"):

                            st.write(
                                "PSD"
                            )

                        elif file_name.endswith(".xlsx"):

                            st.write(
                                "Report"
                            )

                        else:

                            st.write(
                                "-"
                            )

                    with col3:

                        with open(
                            file_path,
                            "rb"
                        ) as file:

                            st.download_button(

                                label="⬇",

                                data=file,

                                file_name=file_name,

                                key=f"{run}_{file_name}"

                            )

            st.divider()

    # =====================================
    # SUMMARY
    # =====================================

    st.success(

        f"Total Analysis Runs : {len(analysis_runs)}"

    )