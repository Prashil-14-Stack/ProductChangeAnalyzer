import streamlit as st
from datetime import datetime


# ==========================================================
# HEADER
# ==========================================================

def render_header():

    username = st.session_state.get(
        "username",
        "Administrator"
    )

    today = datetime.now().strftime("%d/%m/%Y")

    left, right = st.columns([4, 2])

    # ======================================================
    # LEFT
    # ======================================================

    with left:

        st.markdown(
            """
            <h2 style="
            margin:0;
                font-size:42px;
                font-weight:700;
                color:#FFFFFF;
            ">
                Product Change Analyzer
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "AI Powered Product Specification Comparison Platform"
        )

    # ======================================================
    # RIGHT
    # ======================================================

    with right:

        c1, c2, c3 = st.columns(
            [2, 1.3, 1.3],
            vertical_alignment="top"
    )

        #with c1:

        #    st.markdown("##### 📅 Date")
        #    st.info(today)

        with c2:

            st.markdown("##### 🟢 Status")
            st.success("Online")

        with c3:

            st.markdown("##### 👤 User")
            st.info(username)

    #st.divider()
    st.write("")    