import streamlit as st

from pipeline.analysis_pipeline_pdf import AnalysisPipelinePDF


def show_pdf_analysis():

    # ==========================================================
    # Header
    # ==========================================================

    st.markdown(
        """
        <h2 style="
            margin-bottom:3px;
            font-size:36px;
            font-weight:700;
            color:#FFFFFF;
        ">
            📕 PDF Analysis
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Upload Product Specification PDF documents for parameter extraction."
    )

    st.divider()

    # ==========================================================
    # Upload
    # ==========================================================

    uploaded_files = st.file_uploader(

        "Upload Product Specification PDFs",

        type=["pdf"],

        accept_multiple_files=True,

        help="Upload one or more Product Specification PDF documents."

    )

    # ==========================================================
    # Uploaded Files
    # ==========================================================

    if uploaded_files:

        st.subheader(":material/description: Uploaded Documents")

        for i, file in enumerate(uploaded_files, start=1):

            st.write(

                f"**V{i}** → {file.name}"

            )

        st.success(

            f"{len(uploaded_files)} PDF file(s) uploaded."

        )

    # ==========================================================
    # Extract
    # ==========================================================

    if st.button(

        "📄 Extract Business Parameters",

        use_container_width=True

    ):

        if not uploaded_files:

            st.error(

                "Please upload at least one PDF document."

            )

            st.stop()

        try:

            pipeline = AnalysisPipelinePDF()

            result = pipeline.execute(

                uploaded_files

            )

            # ==================================================
            # Metrics
            # ==================================================

            st.divider()

            st.subheader(":material/analytics: Extraction Summary")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(

                    "Documents",

                    result["metrics"]["documents"]

                )

            with col2:

                st.metric(

                    "Business Parameters",

                    result["metrics"]["parameters"]

                )

            # ==================================================
            # Results
            # ==================================================

            st.divider()

            st.subheader(":material/folder: Extracted Parameters")

            for document in result["documents"]:

                st.markdown("---")

                st.markdown(

                    f"## 📄 {document['filename']}"

                )

                st.caption(

                    f"Version {document['version']}"

                )

                if not document["parameters"]:

                    st.warning(

                        "No Business Parameters detected."

                    )

                    continue

                st.success(

                    f"{len(document['parameters'])} parameters extracted."

                )

                # ----------------------------------------------
                # Parameters
                # ----------------------------------------------

                for parameter in document["parameters"]:

                    with st.expander(

                        parameter.name

                    ):

                        st.markdown(

                            f"**Parameter Name**"

                        )

                        st.write(

                            parameter.name

                        )

                        st.markdown(

                            "**Description**"

                        )

                        st.write(

                            parameter.value

                        )

        except Exception as ex:

            st.exception(ex)