import streamlit as st
import textwrap

# ==========================================================
# ENTERPRISE SIDEBAR
# ==========================================================

def render_sidebar():

    with st.sidebar:

        st.markdown("<br>", unsafe_allow_html=True)


        # ==================================================
        # LOGO
        # ==================================================

        st.image("images/bajaj_logo.png", use_container_width=True)

        st.markdown("## Product Change Analyzer")

        st.caption("Enterprise AI Platform")

        st.divider()

        # ==================================================
        # NAVIGATION
        # ==================================================

        st.markdown(
            """
            <div style="
            color:white;
            font-size:15px;
            font-weight:700;
            margin-bottom:12px;
            ">
            Navigation
            </div>
            """,
            unsafe_allow_html=True
        )

        page = st.radio(

            "Navigation",

            [
                "Analysis",

                "Dashboard",

                "Repository",

                "History",

                "Reports",

                "Settings"

            ],

            label_visibility="collapsed"

        )

        st.markdown("---")

        # ==================================================
        # AI SERVICES
        # ==================================================

        st.markdown(
            """
            <div style="
            color:white;
            font-size:15px;
            font-weight:700;
            ">
            AI Services
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("Semantic Matching")

        st.success("Business Understanding")

        st.success("Impact Analyzer")

        st.success("Diff Engine")

        st.success("Excel Generator")

        st.markdown("---")

        # ==================================================
        # STORAGE
        # ==================================================

        st.markdown(
            """
            <div style="
            color:white;
            font-size:15px;
            font-weight:700;
            ">
            Repository Health
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(0.72)

        st.caption("72% Storage Utilized")

        st.markdown("---")

        # ==================================================
        # QUICK STATS
        # ==================================================

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Products",
                "124"
            )

        with c2:

            st.metric(
                "Analyses",
                "39"
            )

        st.markdown("---")

        # ==================================================
        # VERSION
        # ==================================================

        st.markdown(
            """
            <div style="
            text-align:center;
            color:#C7D6E7;
            font-size:12px;
            ">

            Version 2.0

            <br>

            © Bajaj Allianz Life

            </div>
            """,
            unsafe_allow_html=True
        )

        # ==================================================
        # USER
        # ==================================================

        username = st.session_state.get(
            "username",
            "Administrator"
        )

        with st.container():

            st.markdown("### 👤 User")

            st.caption("Currently Logged In")

            st.info(f"**{username}**")

            st.divider()

            # Logout Button
            if st.button(
                "Logout",
                use_container_width=True
            ):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.rerun()

    st.divider()

    return page