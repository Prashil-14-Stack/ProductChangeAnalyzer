import streamlit as st
import os
import json
import subprocess
from datetime import datetime

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logo_path = os.path.join(
    BASE_DIR,
    "images",
    "bajaj_logo.png"
)
# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Product Change Analyzer",
    page_icon="",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "analysis_completed" not in st.session_state:
    st.session_state.analysis_completed = False

if "analysis_completed" not in st.session_state: 
    st.session_state.analysis_completed = False
# =====================================
# STYLING
# =====================================

st.markdown(
    """
    <style>

    .main-title {
        text-align:center;
        color:#0F62FE;
        font-size:45px;
        font-weight:bold;
        margin-bottom:20px;
    }

    .stButton > button {
        width:100%;
        background-color:#0F62FE;
        color:white;
        font-weight:bold;
        border-radius:8px;
        height:50px;
    }

    .stDownloadButton > button {
        width:100%;
        background-color:#198754;
        color:white;
        font-weight:bold;
        border-radius:8px;
        height:50px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

if not st.session_state.logged_in:

    # =====================================
    # HEADER
    # =====================================

    st.markdown(
        """
        <div style='
            background:#5BC0EB;
            padding:-30px;
            border-radius:5px;
            text-align:center;
            '>

        <h1 style='
            color:black;
            font-size:40px;
            margin:0;'>
            Product Change Analyzer
        </h1>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # =====================================
    # PAGE LAYOUT
    # =====================================

    left, right = st.columns([1.3,1])

    # =====================================
    # LEFT SIDE
    # =====================================
    # Create two columns

    with left:

        st.image(
            logo_path,
            width=350
        )

        st.markdown(
            """


            
            
            
            
            """
        
        )
        # =====================================
        # RIGHT SIDE
        # =====================================

        with right:

            st.markdown("## Login")

            username = st.text_input(
                "Username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            st.write("")

            if st.button(
                "🔐 Login"
            ):

                if (
                    username == "admin"
                    and
                    password == "admin123"
                ):

                    st.session_state.logged_in = True
                    st.session_state.user_name = username
                    st.rerun()

                else:

                    st.error(
                        "Invalid Credentials"
                    )

        st.stop()
# =====================================
# CREATE FOLDERS
# =====================================

from config import BUCKET_FOLDER

os.makedirs(
    BUCKET_FOLDER,
    exist_ok=True
)

import os
from config import UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

from config import OUTPUT_FOLDER

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

# =====================================
# TITLE
# =====================================

st.markdown(
    """
    <div class="main-title">
        Product Change Analyzer
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(
    [8, 1]
)

with col1:

    st.write(
        f"👤 Logged In As: {st.session_state.user_name}"
    )

with col2:

    if st.button(
        "Logout"
    ):

        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.analysis_completed = False
        st.rerun()

st.divider()

# =====================================
# FILE UPLOADS
# =====================================

st.subheader(
    "Upload Product Specifications"
)

left, right = st.columns(2)

with left:

    v1_file = st.file_uploader(
        "Upload Version 1 PSD",
        type=["docx", "pdf"]
    )

with right:

    v2_file = st.file_uploader(
        "Upload Version 2 PSD",
        type=["docx", "pdf"]
    )

# =====================================
# ANALYZE BUTTON
# =====================================

if st.button(
    "Analyze Product Changes"
):

    if (
        v1_file is None
        or
        v2_file is None
    ):

        st.error(
            "Please upload both documents."
        )

    else:

        with open(
            "uploads/v1.docx",
            "wb"
        ) as file:

            file.write(
                v1_file.getbuffer()
            )

        with open(
            "uploads/v2.docx",
            "wb"
        ) as file:

            file.write(
                v2_file.getbuffer()
            )

        timestamp = datetime.now().strftime(
             "%Y%m%d_%H%M%S"
        )

        analysis_folder = (
            f"bucket/Analysis_{timestamp}"
        )

        os.makedirs(
            analysis_folder,
            exist_ok=True
        )

        with open(
            f"{analysis_folder}/v1.docx",
            "wb"
        ) as file:

            file.write(
                v1_file.getbuffer()
            )

        with open(
            f"{analysis_folder}/v2.docx",
            "wb"
        ) as file:

            file.write(
                v2_file.getbuffer()
            )

        st.info(
            "🤖 Running AI Analysis..."
        )

        try:

            result = subprocess.run(
                [
                  "python3",
                  "test_v2_report.py"
                ],
                capture_output=True,
                text=True
            )

            st.success(
               "✅ Analysis Complete"
             )
           
            # IMPORTANT
            st.session_state.analysis_completed = True

            import shutil

            if os.path.exists(
                "comparison_v4.xlsx"
            ):

                shutil.copy(
                    "comparison_v4.xlsx",
                    f"{analysis_folder}/comparison_v4.xlsx"
                )   
            if result.stderr:

                if "HF Hub" not in result.stderr:

                    st.warning(
                        result.stderr
        )
        except Exception as e:

            st.error(
                str(e)
            )

st.divider()

# =====================================
# KPI SECTION
# =====================================

st.subheader(
    "Analysis Summary"
)

parameters_compared = 0
matches_found = 0
new_parameters = 0
review_required = 0
effort_saving = "0%"

if (
    st.session_state.analysis_completed
    and
    os.path.exists("outputs/summary.json")
):

    with open(
        "outputs/summary.json",
        "r"
    ) as file:

        summary = json.load(file)

    parameters_compared = summary.get(
        "parameters_compared",
        0
    )

    matches_found = summary.get(
        "matches_found",
        0
    )

    new_parameters = summary.get(
        "new_parameters",
        0
    )

    review_required = summary.get(
        "review_required",
        0
    )

    effort_saving = summary.get(
        "effort_saving",
        "0%"
    )

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.metric(
        "📊 Parameters Compared",
        parameters_compared
    )

with c2:

    st.metric(
        "🎯 Matches Found",
        matches_found
    )

with c3:

    st.metric(
        "🆕 New Parameters",
        new_parameters
    )

with c4:

    st.metric(
        "⚠️ Requires Review",
        review_required
    )

with c5:

    st.metric(
        "🚀 Effort Saving",
        effort_saving
    )

st.divider()

import pandas as pd

st.subheader(":material/table_chart:Comparison Preview")

if (
    st.session_state.analysis_completed
    and
    os.path.exists("comparison_v4.xlsx")
):

    df = pd.read_excel(
        "comparison_v4.xlsx"
    )

    st.dataframe(
        df.head(3),
        use_container_width=True
    )

else:

    st.info(
        "Run an analysis to preview the comparison results."
    )


# =====================================
# DOWNLOAD REPORT
# =====================================

st.subheader(":material/download:Download Results")

if os.path.exists(
    "comparison_v4.xlsx"
):

    with open(
        "comparison_v4.xlsx",
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download Excel Report",
            data=file,
            file_name="comparison_v4.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:

    st.info(
        "Generate a report first."
    )
# =====================================
# REPOSITORY
# =====================================
    from components.ui import page_title
    
    page_title(
        ":material/folder: Document Repository",
        "Browse previous analysis runs and download associated documents."
    )

header1, header2, header3, header4 = st.columns(
    [4, 2, 2, 1]
)

header1.markdown("**Document**")
header2.markdown("**User**")
header3.markdown("**Uploaded**")
header4.markdown("**Download**")

analysis_runs = sorted(
    os.listdir("bucket"),
    reverse=True
)

if len(analysis_runs) == 0:

    st.info(
        "No analysis runs available."
    )

else:

    for run in analysis_runs:

        run_path = os.path.join(
            "bucket",
            run
        )

        if not os.path.isdir(
            run_path
        ):
            continue

        with st.expander(
            f"📁 {run}"
        ):

            run_time = datetime.fromtimestamp(
                os.path.getctime(run_path)
            )

            st.write(
                f"👤 User: {st.session_state.user_name}"
            )

            st.write(
                f"📅 Date: {run_time.strftime('%d-%b-%Y %H:%M')}"
            )

            st.write(
                "✅ Status: Completed"
            )

            st.divider()

            run_files = os.listdir(
                run_path
            )

            for file_name in run_files:

                file_path = os.path.join(
                    run_path,
                    file_name
                )

                col1, col2 = st.columns(
                    [5, 1]
                )

                with col1:

                    st.write(
                        file_name
                    )

                with col2:

                    with open(
                        file_path,
                        "rb"
                    ) as file:

                        st.download_button(
                            "⬇️",
                            data=file,
                            file_name=file_name,
                            key=f"{run}_{file_name}"
                        )