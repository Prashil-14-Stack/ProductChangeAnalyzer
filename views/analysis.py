import streamlit as st

from services.analysis_service import AnalysisService

from utils.session_manager import SessionManager

def show_analysis():

    st.markdown(
        """
        <h2 style="
            margin-bottom:3px;
            font-size:36px;
            font-weight:700;
            color:#FFFFFF;
        ">
            🤖 New Analysis
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Upload Product Specification Documents in chronological order."
    )

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload Product Versions",
        type=["docx", "pdf"],
        accept_multiple_files=True,
        help="Select Version 1, Version 2, Version 3... in chronological order."
    )

    analysis = SessionManager.get_analysis()
    
    #st.divider()

    # ==========================================================
    # EXISTING ANALYSIS
    # ==========================================================

    if analysis:

        st.info("📂 Showing current analysis. Click 'Start New Analysis' to analyze different documents.")

        if not analysis and st.button("🆕 Start New Analysis"):

            SessionManager.clear_analysis()

            st.rerun()

        st.subheader(":material/description: Uploaded Files")

        for document in analysis["documents"]:

            st.write(
                f"**V{document['version']}** → {document['filename']}"
            )

        st.success(
            f"{len(analysis['documents'])} files available."
        )

        st.subheader(":material/sync_alt: Planned Comparison")

        for comparison in analysis["comparisons"]:

            st.write(

                f"✅ V{comparison['source']['version']} "
                f"({comparison['source']['filename']}) → "
                f"V{comparison['target']['version']} "
                f"({comparison['target']['filename']})"

            )

        st.subheader(":material/analytics: Parameter Comparison")

        st.dataframe(

            analysis["comparison_table"],

            use_container_width=True

        )

        with open(analysis["report_path"], "rb") as file:

            st.download_button(

                "📥 Download Analysis Report",

                data=file,

                file_name="Product_Analysis_Report.xlsx",

                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                use_container_width=True

            )

    # ==========================================================
    # NEW UPLOAD
    # ==========================================================

    elif uploaded_files:

        st.subheader(":material/description: Uploaded Files")

        for i, file in enumerate(uploaded_files, start=1):

            st.write(f"**V{i}** → {file.name}")

        if len(uploaded_files) >= 2:

            st.success(
                f"{len(uploaded_files)} files uploaded successfully."
            )

            st.subheader(":material/sync_alt: Planned Comparison")

            for i in range(len(uploaded_files)-1):

                st.write(

                    f"✅ V{i+1} ({uploaded_files[i].name}) → "
                    f"V{i+2} ({uploaded_files[i+1].name})"

                )

        else:

            st.warning(
                "Upload at least two versions."
            )
    if st.button(
        "🚀 Analyze Product Changes",
        use_container_width=True
        ):

        if not uploaded_files or len(uploaded_files) < 2:

            st.error(
                "Please upload at least two Product Specification Documents."
            )

        else:

            try:

                service = AnalysisService()

                result = service.analyze(
                    uploaded_files
                )

                # ----------------------------------------------------
                # Save the complete analysis
                # ----------------------------------------------------

                SessionManager.save_analysis(result)

                # ----------------------------------------------------
                # Success
                # ----------------------------------------------------

                st.success(
                    "✅ AI Analysis Completed Successfully."
                )

                # ----------------------------------------------------
                # Show Comparison
                # ----------------------------------------------------

                st.subheader(":material/analytics: Parameter Comparison")

                st.dataframe(
                    result["comparison_table"],
                    use_container_width=True
                )

                # ----------------------------------------------------
                # Download Report
                # ----------------------------------------------------

                with open(result["report_path"], "rb") as file:

                    st.download_button(

                        "📥 Download Analysis Report",

                        data=file,

                        file_name="Product_Analysis_Report.xlsx",

                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                        use_container_width=True,

                        key="download_report"

                    )

            except Exception as e:

                st.exception(e)