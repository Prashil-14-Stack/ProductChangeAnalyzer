import xlsxwriter


class ExcelGeneratorV2:

    def generate_report(

            self,

            documents,

            comparison_table,

            analysis_results,

            file_name

    ):

        # =====================================================
        # Create Workbook
        # =====================================================

        workbook = xlsxwriter.Workbook(file_name)

        worksheet = workbook.add_worksheet("Parameter Comparison")

        # =====================================================
        # Cell Formats
        # =====================================================

        header_format = workbook.add_format({

            "bold": True,

            "font_color": "white",

            "bg_color": "#1F4E78",

            "align": "center",

            "valign": "vcenter",

            "text_wrap": True,

            "border": 1

        })

        normal_format = workbook.add_format({

            "text_wrap": True,

            "valign": "top",

            "border": 1

        })

        # =====================================================
        # Headers
        # =====================================================

        headers = [

            "Source Version",

            "Target Version",

            "V1 Parameter",

            "Matched V2 Parameter",

            "Parameter Confidence",

            "Description Confidence",

            "Overall Confidence",

            "Decision",

            "Status",

            "Change Type",

            "Severity",

            "Remarks",

            "V1 Content",

            "V2 Content",

            "Difference"

        ]

        # Write Header Row

        for column, header in enumerate(headers):

            worksheet.write(

                0,

                column,

                header,

                header_format

            )

        # =====================================================
        # Write Data
        # =====================================================

        row_number = 1

        for row in comparison_table:

            values = [

                row.get("Source Version"),

                row.get("Target Version"),

                row.get("V1 Parameter"),

                row.get("Matched V2 Parameter"),

                row.get("Parameter Confidence"),

                row.get("Description Confidence"),

                row.get("Overall Confidence"),

                row.get("Decision"),

                row.get("Status"),

                row.get("Change Type"),

                row.get("Severity"),

                row.get("Remarks"),

                row.get("V1"),

                row.get("V2"),

                row.get("Difference")

            ]

            for column, value in enumerate(values):

                worksheet.write(

                    row_number,

                    column,

                    value,

                    normal_format

                )

            row_number += 1

        # =====================================================
        # Column Widths
        # =====================================================

        worksheet.set_column(0, 0, 15)

        worksheet.set_column(1, 1, 15)

        worksheet.set_column(2, 3, 30)

        worksheet.set_column(4, 6, 18)

        worksheet.set_column(7, 10, 20)

        worksheet.set_column(11, 11, 50)

        worksheet.set_column(12, 13, 80)

        worksheet.set_column(14, 14, 40)

        # =====================================================
        # Close Workbook
        # =====================================================

        workbook.close()

        return file_name