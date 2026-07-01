import streamlit as st

from utils.session_manager import SessionManager

def render_cards():
    analysis = SessionManager.get_analysis()

    if analysis:

        metrics = analysis["metrics"]

    else:

        metrics = {

            "parameters":0,

            "matches":0,

            "changes":0,

            "repository":0,

            "accuracy":0

        }
# ==========================================================
# KPI DASHBOARD
# ==========================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "📄 Parameters",
            metrics["parameters"]
        )

    with col2:
        st.metric(
            "🎯 Matches",
            metrics["matches"]
        )

    with col3:
        st.metric(
            "⚠ Changes",
            metrics["changes"]
        )

    with col4:
        st.metric(
            "📂 Repository",
            metrics["repository"]
        )

    with col5:
        st.metric(
            "🎯 AI Accuracy",
            f"{metrics['accuracy']}%"
        )