import streamlit as st
from pathlib import Path


def load_css():

    st.markdown("""
    <style>

    h1{
        font-size:42px !important;
        font-weight:700 !important;
        margin-bottom:8px !important;
    }

    h2{
        font-size:30px !important;
        font-weight:600 !important;
    }

    h3{
        font-size:22px !important;
        font-weight:600 !important;
    }

    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# LOAD GLOBAL CSS
# ==========================================================

def load_css():

    css_file = Path("assets/styles.css")

    if css_file.exists():

        with open(css_file, "r", encoding="utf-8") as f:

            st.markdown(

                f"""
                <style>
                {f.read()}
                </style>
                """,

                unsafe_allow_html=True

            )


# ==========================================================
# PAGE TITLE
# ==========================================================

def page_title(
    title,
    subtitle=""
):

    st.markdown(

        f"""
        <div class="enterprise-header">

            <h1 style="margin-bottom:5px;">
                {title}
            </h1>

            <p style="
            margin-top:0;
            font-size:16px;
            ">
            {subtitle}
            </p>

        </div>

        <br>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# SECTION TITLE
# ==========================================================

def section_title(title):

    st.markdown(

        f"""
        <h3 style="
        margin-top:20px;
        margin-bottom:15px;
        color:#1F2937;
        ">
        {title}
        </h3>
        """,

        unsafe_allow_html=True

    )


# ==========================================================
# CARD START
# ==========================================================

def card_start():

    st.markdown(

        """
        <div class="card">
        """,

        unsafe_allow_html=True

    )


# ==========================================================
# CARD END
# ==========================================================

def card_end():

    st.markdown(

        """
        </div>
        """,

        unsafe_allow_html=True

    )


# ==========================================================
# INFORMATION CARD
# ==========================================================

def info_card(
    title,
    value,
    subtitle=""
):

    st.markdown(

        f"""
        <div class="card">

            <div style="
            color:#6B7280;
            font-size:14px;
            font-weight:600;
            ">

            {title}

            </div>

            <div style="
            font-size:36px;
            font-weight:700;
            color:#005BAC;
            margin-top:8px;
            ">

            {value}

            </div>

            <div style="
            color:#6B7280;
            margin-top:6px;
            ">

            {subtitle}

            </div>

        </div>
        """,

        unsafe_allow_html=True

    )


# ==========================================================
# STATUS BADGE
# ==========================================================

def status_badge(
    text,
    color="#22C55E"
):

    st.markdown(

        f"""
        <span style="
        background:{color};
        color:white;
        padding:6px 14px;
        border-radius:20px;
        font-size:13px;
        font-weight:600;
        ">

        {text}

        </span>
        """,

        unsafe_allow_html=True

    )


# ==========================================================
# HORIZONTAL SPACE
# ==========================================================

def vertical_space(lines=1):

    st.markdown(
        "<br>" * lines,
        unsafe_allow_html=True
    )


# ==========================================================
# DIVIDER
# ==========================================================

def divider():

    st.markdown(
        "<hr>",
        unsafe_allow_html=True
    )


# ==========================================================
# SUCCESS PANEL
# ==========================================================

def success_panel(message):

    st.markdown(

        f"""
        <div style="
        background:#ECFDF5;
        border-left:5px solid #22C55E;
        padding:16px;
        border-radius:12px;
        margin-bottom:15px;
        ">

        ✅ {message}

        </div>
        """,

        unsafe_allow_html=True

    )


# ==========================================================
# WARNING PANEL
# ==========================================================

def warning_panel(message):

    st.markdown(

        f"""
        <div style="
        background:#FFF7ED;
        border-left:5px solid #F59E0B;
        padding:16px;
        border-radius:12px;
        margin-bottom:15px;
        ">

        ⚠ {message}

        </div>
        """,

        unsafe_allow_html=True

    )


# ==========================================================
# ERROR PANEL
# ==========================================================

def error_panel(message):

    st.markdown(

        f"""
        <div style="
        background:#FEF2F2;
        border-left:5px solid #EF4444;
        padding:16px;
        border-radius:12px;
        margin-bottom:15px;
        ">

        ❌ {message}

        </div>
        """,

        unsafe_allow_html=True

    )


# ==========================================================
# PAGE FOOTER
# ==========================================================

def page_footer():

    st.markdown(

        """
        <br><br>

        <div style="
        text-align:center;
        color:#6B7280;
        font-size:13px;
        ">

        Product Change Analyzer
        <br>
        Enterprise AI Platform
        <br>
        Version 2.0

        </div>

        """,

        unsafe_allow_html=True

    )