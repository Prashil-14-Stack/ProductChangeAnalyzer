import streamlit as st


class SessionManager:

    @staticmethod
    def save_analysis(result):

        st.session_state["current_analysis"] = result

    @staticmethod
    def get_analysis():

        return st.session_state.get(
            "current_analysis",
            None
        )

    @staticmethod
    def clear_analysis():

        if "current_analysis" in st.session_state:
            del st.session_state["current_analysis"]

    @staticmethod
    def has_analysis():

        return "current_analysis" in st.session_state