import streamlit as st
import os
import shutil


def show_settings():

    from components.ui import page_title

    page_title(
        ":material/settings: Settings",
        "Manage application settings and user preferences."
    )

    # =====================================
    # USER PROFILE
    # =====================================

    st.subheader(
        "👤 User Profile"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(

            "Username",

            value=st.session_state.username,

            disabled=True

        )

        st.text_input(

            "Role",

            value="Business Analyst",

            disabled=True

        )

    with col2:

        st.text_input(

            "Application",

            value="Product Change Analyzer",

            disabled=True

        )

        st.text_input(

            "Version",

            value="1.0",

            disabled=True

        )

    st.divider()

    # =====================================
    # APPLICATION SETTINGS
    # =====================================

    st.subheader(
        "⚙ Application Settings"
    )

    dark_mode = st.toggle(
        "Enable Dark Mode",
        value=False
    )

    notifications = st.toggle(
        "Enable Notifications",
        value=True
    )

    auto_download = st.toggle(
        "Auto Download Reports",
        value=False
    )

    st.divider()

    # =====================================
    # STORAGE
    # =====================================

    st.subheader(
        "📂 Storage"
    )

    bucket_size = 0

    if os.path.exists("bucket"):

        for root, dirs, files in os.walk("bucket"):

            for file in files:

                file_path = os.path.join(
                    root,
                    file
                )

                bucket_size += os.path.getsize(
                    file_path
                )

    bucket_size = bucket_size / (1024 * 1024)

    st.metric(

        "Repository Size",

        f"{bucket_size:.2f} MB"

    )

    st.divider()

    # =====================================
    # CLEAR OUTPUTS
    # =====================================

    st.subheader(
        "🧹 Maintenance"
    )

    if st.button(
        "Clear Outputs"
    ):

        if os.path.exists("outputs"):

            shutil.rmtree(
                "outputs"
            )

        from config import UPLOAD_FOLDER

        os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
        )

        st.success(
            "Outputs folder cleared successfully."
        )

    if st.button(
        "Clear Uploads"
    ):

        if os.path.exists("uploads"):

            shutil.rmtree(
                "uploads"
            )

        from config import UPLOAD_FOLDER

        os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
        )

        st.success(
            "Uploads folder cleared successfully."
        )

    st.divider()

    # =====================================
    # ABOUT
    # =====================================

    st.subheader(
        "ℹ About"
    )

    st.info(
        """
        **Product Change Analyzer**

        AI Powered Product Specification
        Comparison Platform

        Developed for:

        • Product Team

        • Business Analysts

        • Operations

        • Actuarial Team

        Version: 1.0
        """
    )

    st.divider()

    # =====================================
    # LOGOUT
    # =====================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.rerun()