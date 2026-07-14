import streamlit as st

from pipeline.analysis_pipeline_docx import AnalysisPipelineDOCX

from utils.session_manager import SessionManager


def show_analysis():

    # ==========================================================
    # PAGE HEADER
    # ==========================================================

    st.markdown(
        """
        <h2 style="
            margin-bottom:3px;
            font-size:36px;
            font-weight:700;
            color:#FFFFFF;
        ">
            🤖 Product Change Analyzer
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.write(

        "Upload Product Specification Documents in chronological order."

    )

    st.divider()

    # ==========================================================
    # ANALYSIS MODE
    # ==========================================================

    analysis_mode = st.radio(

        "Select Analysis Mode",

        [

            "DOCX",

            "PDF",

            "Mixed"

        ],

        horizontal=True

    )

    # ==========================================================
    # FILE UPLOADER
    # ==========================================================

    uploaded_files = st.file_uploader(

        "Upload Product Versions",

        type=["docx", "pdf"],

        accept_multiple_files=True,

        help=(

            "DOCX Mode → Upload DOCX files only\n"

            "PDF Mode → Upload PDF files only\n"

            "Mixed Mode → Upload any combination"

        ),

        key="main_file_uploader"

    )

    analysis = SessionManager.get_analysis()

    # ==========================================================
    # EXISTING ANALYSIS
    # ==========================================================

    if analysis:

        st.info(

            "📂 Showing existing analysis."

        )

        col1, col2 = st.columns(

            [4, 1]

        )

        with col2:

            if st.button(

                "🆕 New Analysis",

                use_container_width=True

            ):

                SessionManager.clear_analysis()

                st.rerun()

        st.subheader(

            ":material/description: Uploaded Files"

        )

        for document in analysis["documents"]:

            st.write(

                f"**V{document['version']}** → "

                f"{document['filename']}"

            )

        st.success(

            f"{len(analysis['documents'])} "

            f"files available."

        )

        st.subheader(

            ":material/sync_alt: Planned Comparison"

        )

        for comparison in analysis["comparisons"]:

            st.write(

                f"✅ "

                f"V{comparison['source']['version']} "

                f"({comparison['source']['filename']})"

                f" → "

                f"V{comparison['target']['version']} "

                f"({comparison['target']['filename']})"

            )

        st.subheader(

            ":material/analytics: Parameter Comparison"

        )

        st.dataframe(

            analysis["comparison_table"],

            use_container_width=True

        )

        with open(

            analysis["report_path"],

            "rb"

        ) as file:

            st.download_button(

                "📥 Download Analysis Report",

                data=file,

                file_name="Product_Analysis_Report.xlsx",

                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                use_container_width=True

            )

        return

    # ==========================================================
    # NEW UPLOAD
    # ==========================================================

    if uploaded_files:

        st.subheader(

            ":material/description: Uploaded Files"

        )

        for i, file in enumerate(

            uploaded_files,

            start=1

        ):

            st.write(

                f"**V{i}** → {file.name}"

            )

        if len(uploaded_files) >= 2:

            st.success(

                f"{len(uploaded_files)} "

                f"files uploaded successfully."

            )

            st.subheader(

                ":material/sync_alt: Planned Comparison"

            )

            for i in range(

                len(uploaded_files)-1

            ):

                st.write(

                    f"✅ "

                    f"V{i+1} "

                    f"({uploaded_files[i].name})"

                    f" → "

                    f"V{i+2} "

                    f"({uploaded_files[i+1].name})"

                )

        else:

            st.warning(

                "Upload at least two versions."

            )
    # ==========================================================
    # ANALYZE BUTTON
    # ==========================================================

    if st.button(

        "🚀 Analyze Product Changes",

        use_container_width=True

    ):

        # ------------------------------------------------------
        # Validate Upload
        # ------------------------------------------------------

        if not uploaded_files or len(uploaded_files) < 2:

            st.error(

                "Please upload at least two Product Specification Documents."

            )

            st.stop()

        # ------------------------------------------------------
        # Validate File Types
        # ------------------------------------------------------

        if analysis_mode == "DOCX":

            invalid = [

                file.name

                for file in uploaded_files

                if not file.name.lower().endswith(".docx")

            ]

            if invalid:

                st.error(

                    "DOCX mode accepts only DOCX files.\n\n"

                    f"Invalid Files:\n\n{chr(10).join(invalid)}"

                )

                st.stop()

        elif analysis_mode == "PDF":

            invalid = [

                file.name

                for file in uploaded_files

                if not file.name.lower().endswith(".pdf")

            ]

            if invalid:

                st.error(

                    "PDF mode accepts only PDF files.\n\n"

                    f"Invalid Files:\n\n{chr(10).join(invalid)}"

                )

                st.stop()

        # Mixed Mode
        # No validation required

        # ------------------------------------------------------
        # Pipeline Selection
        # ------------------------------------------------------

        if analysis_mode == "DOCX":

            pipeline = AnalysisPipelineDOCX()

        elif analysis_mode == "PDF":

            from v2.services.product_change_service import ProductChangeService

            pipeline = ProductChangeService()

        elif analysis_mode == "Mixed":

            st.info(
                "🚧 Mixed Pipeline is under development."
            )

            st.stop()

        # ------------------------------------------------------
        # Execute Pipeline
        # ------------------------------------------------------

        try:

            from config.report_config import (

                REPORT_FOLDER,

                REPORT_NAME

            )

            report_path = (

                f"{REPORT_FOLDER}/{REPORT_NAME}"

            )

            with st.spinner("Analyzing Product Specifications..."):

                if analysis_mode == "DOCX":

                    result = pipeline.execute(

                        uploaded_files,

                        report_path

                    )

                elif analysis_mode == "PDF":

                    result = pipeline.compare_products(

                        uploaded_files[0],

                        uploaded_files[1]

                    )

                else:

                    st.error("Unsupported analysis mode.")

                    st.stop()

            # --------------------------------------------------
            # Save Session
            # --------------------------------------------------

            SessionManager.save_analysis(

                result

            )

            st.success(

                "✅ AI Analysis Completed Successfully."

            )

            # --------------------------------------------------
            # Show Comparison
            # --------------------------------------------------

            st.subheader(

                ":material/analytics: Parameter Comparison"

            )

            st.dataframe(

                result["comparison_table"],

                use_container_width=True

            )

            # --------------------------------------------------
            # Dashboard Metrics
            # --------------------------------------------------

            if "metrics" in result:

                metrics = result["metrics"]

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(

                        "Parameters",

                        metrics["parameters"]

                    )

                with col2:

                    st.metric(

                        "Matches",

                        metrics["matches"]

                    )

                with col3:

                    st.metric(

                        "Changes",

                        metrics["changes"]

                    )

                with col4:

                    st.metric(

                        "Documents",

                        metrics["repository"]

                    )

            # --------------------------------------------------
            # Download Report
            # --------------------------------------------------

            with open(

                result["report_path"],

                "rb"

            ) as file:

                st.download_button(

                    "📥 Download Analysis Report",

                    data=file,

                    file_name="Product_Analysis_Report.xlsx",

                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                    use_container_width=True,

                    key="download_report"

                )

        # --------------------------------------------------
        # Auto Refresh
        # --------------------------------------------------

            st.divider()

            if st.button(

                "🔄 Refresh Analysis",

                use_container_width=True,

                key="refresh_analysis"

            ):

                st.rerun()

            # --------------------------------------------------
            # End of Successful Execution
            # --------------------------------------------------

            return

            # --------------------------------------------------
            # Exception Handling
            # --------------------------------------------------

        except Exception as ex:

                st.error(

                    "❌ Analysis Failed"

                )

                with st.expander(

                    "View Technical Details"

                ):

                    st.exception(

                        ex

                    )

                st.info(

                    """
                    Possible Reasons

                    • Unsupported document structure

                    • Corrupted document

                    • Missing parameters

                    • AI service unavailable

                    • Internal processing error
                    """

                )

                return

        # ==========================================================
        # Footer
        # ==========================================================

        st.divider()

        col1, col2 = st.columns([3, 2])

        with col1:

            st.caption(

                "Product Change Analyzer • Enterprise AI Platform"

            )

        with col2:

            st.caption(

                f"Mode : {analysis_mode}"

            )