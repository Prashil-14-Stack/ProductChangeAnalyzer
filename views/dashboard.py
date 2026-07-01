import streamlit as st
from components.cards import render_cards
from components.tables import render_recent_analysis


def show_dashboard():

    # =====================================
    # PAGE TITLE
    # =====================================
    from components.ui import page_title

    page_title(
        ":material/dashboard: Dashboard",
        "Welcome to the AI Powered Product Change Analyzer."
    )

    # =====================================
    # KPI CARDS
    # =====================================

    render_cards()

    st.divider()

    # =====================================
    # QUICK ACTIONS
    # =====================================

    st.subheader(":material/bolt: Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
            📤 **New Analysis**

            Upload two Product
            Specification Documents
            and compare changes.
            """
        )

    with col2:

        st.success(
            """
            📂 **Repository**

            Browse all previous
            analysis runs and
            download reports.
            """
        )

    with col3:

        st.warning(
            """
            📑 **Reports**

            View generated
            comparison reports
            and AI insights.
            """
        )

    st.divider()

    # =====================================
    # RECENT ANALYSIS
    # =====================================

    render_recent_analysis()

    st.divider()

    # =====================================
    # DASHBOARD LAYOUT
    # =====================================

    left, right = st.columns([2, 1])

    # =====================================
    # ACTIVITY
    # =====================================

    with left:

        st.subheader(":material/notifications: Recent Activity")

        st.write("• AI Comparison Engine Ready")

        st.write("• Semantic Matching Enabled")

        st.write("• Product Understanding Loaded")

        st.write("• Impact Analyzer Loaded")

        st.write("• Excel Report Generator Ready")

    # =====================================
    # AI STATUS
    # =====================================

    with right:

        st.subheader(":material/psychology: AI Engine")

        st.success("Semantic Matcher")

        st.success("Business Reasoner")

        st.success("Impact Analyzer")

        st.success("Product Understanding")

        st.success("Excel Generator")

    st.divider()

    # =====================================
    # SYSTEM STATUS
    # =====================================

    st.subheader(":material/monitor_heart: System Status")

    status1, status2, status3 = st.columns(3)

    with status1:

        st.metric(
            "Application",
            "Running"
        )

    with status2:

        st.metric(
            "AI Engine",
            "Online"
        )

    with status3:

        st.metric(
            "Version",
            "1.0"
        )