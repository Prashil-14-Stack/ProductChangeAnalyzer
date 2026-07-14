import streamlit as st
import textwrap

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Product Change Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD GLOBAL CSS
# ==========================================================

#from components.styles import load_css

#load_css()

# ==========================================================
# IMPORT COMPONENTS
# ==========================================================

from components.header import render_header

import components.header

#st.write("HEADER FILE:", components.header.__file__)

from components.sidebar import render_sidebar

# ==========================================================
# IMPORT VIEWS
# ==========================================================

from views.dashboard import show_dashboard
from views.analysis import show_analysis
from views.repository import show_repository
from views.reports import show_reports
from views.history import show_history
from views.settings import show_settings

# ==========================================================
# SESSION STATE
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ==========================================================
# DEMO USERS
# ==========================================================

users = {

    "prashil": "1234",

    "manager": "manager123",

    "admin": "admin123",

    "vp": "vp123",

    "uat": "uat123"

}
# ==========================================================
# LOGIN SCREEN
# ==========================================================

def login_screen():

    st.markdown(
        textwrap.dedent(

        """
        <style>

    .login-title{

        text-align:center;

        color:white;

        font-size:34px;

        font-weight:700;

    }

        .login-subtitle{

            text-align:center;

            color:white;

            font-size:18px;

            margin-top:-10px;

        }

        </style>
        """),
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
        background:#005BAC;
        padding:22px 40px;
        border-radius:16px;
        margin-bottom:20px;
        ">

        <div class="login-title">

        Product Change Analyzer

        </div>

        <div class="login-subtitle">

        AI Powered Product Intelligence Platform

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([1, 1.4])

    # ======================================================
    # LEFT PANEL
    # ======================================================

    #with left:
            
       # st.image(
       #    "images/bajaj_logo.png",
       #     width=320   
       # )

        #st.markdown("<br>", unsafe_allow_html=True)
    with left:

        st.markdown("## 🏢 Bajaj Allianz Life Insurance")

        st.markdown(
            """
            ### Enterprise AI Features

            ✅ Semantic Parameter Matching

            ✅ AI Product Comparison

            ✅ Business Impact Assessment

            ✅ Excel Report Generation
            """
        )
    
        #st.info(
           # """
           # ### Enterprise AI Features

          #  ✔ Semantic Parameter Matching

          #  ✔ Business Understanding Engine

          #  ✔ Product Comparison

          #  ✔ Impact Analysis

          #  ✔ Excel Report Generator
          #  """
        #)

    # ======================================================
    # RIGHT PANEL
    # ======================================================

    with right:

        st.markdown(
            """
            <div class="card">
            """,
            unsafe_allow_html=True
        )

        st.subheader("Sign In")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        st.write("")

        if st.button(
            "Sign In",
            use_container_width=True
        ):

            if username.lower() in users and password == users[username.lower()]:

                st.session_state.logged_in = True

                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.stop()

# ==========================================================
# LOGIN
# ==========================================================

if not st.session_state.logged_in:

    login_screen()

# ==========================================================
# MAIN APPLICATION
# ==========================================================

render_header()

page = render_sidebar()

#st.write("Sidebar loaded")

# ==========================================================
# ROUTING
# ==========================================================

if page == "Dashboard":

    show_dashboard()

elif page == "Repository":

    show_repository()

elif page == "Analysis":

    show_analysis()

elif page == "History":

    show_history()

elif page == "Reports":

    show_reports()

elif page == "Settings":

    show_settings()

else:

    show_dashboard()

