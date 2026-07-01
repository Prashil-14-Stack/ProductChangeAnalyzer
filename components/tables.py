import streamlit as st
import pandas as pd
import os


# =====================================
# TOP 5 COMPARISON RESULTS
# =====================================

def render_recent_analysis():

    st.subheader(":material/table_chart: Recent Analysis")

    if not os.path.exists(
        "comparison_v4.xlsx"
    ):

        st.info(
            "No analysis has been performed yet."
        )

        return

    try:

        df = pd.read_excel(
            "comparison_v4.xlsx"
        )

        st.dataframe(

            df.head(5),

            use_container_width=True,

            hide_index=True

        )

    except Exception as e:

        st.error(

            f"Unable to load comparison report.\n\n{e}"

        )


# =====================================
# HISTORY TABLE
# =====================================

def render_history_table(history_df):

    st.subheader(":material/history: Analysis History")

    if history_df.empty:

        st.info(
            "No history available."
        )

        return

    st.dataframe(

        history_df,

        use_container_width=True,

        hide_index=True

    )


# =====================================
# REPOSITORY TABLE
# =====================================

def render_repository_table(repository_df):


    st.subheader(":material/folder: Repository")

    if repository_df.empty:

        st.info(
            "No documents found."
        )

        return

    st.dataframe(

        repository_df,

        use_container_width=True,

        hide_index=True

    )


# =====================================
# REPORT TABLE
# =====================================

def render_report_table(report_df):

    st.subheader(":material/description: Reports")

    if report_df.empty:

        st.info(
            "No reports available."
        )

        return

    st.dataframe(

        report_df,

        use_container_width=True,

        hide_index=True

    )