import xlsxwriter

class ExcelGenerator:


    def generate_report(
            self,
            matching_results,
            comparison_results,
            impact_results,
            understanding_results,
            file_name):

        wworkbook = xlsxwriter.Workbook(file_name)

        # =====================================
        # SHEET 1
        # PARAMETER MATCHING AUDIT
        # =====================================

        sheet1 = workbook.active

        sheet1.title = "Parameter Matching Audit"

        sheet1.append([

            "V1 Parameter",

            "Suggested Match",

            "Confidence",

            "Business Concept",

            "Reason",

            "Review Required"

        ])

        for row in matching_results:

            sheet1.append([

                row["V1 Parameter"],

                row["Suggested Match"],

                row["Confidence"],

                row["Business Concept"],

                row["Reason"],

                row["Review Required"]

            ])

        # =====================================
        # SHEET 2
        # DETAILED COMPARISON
        # =====================================

        sheet2 = workbook.create_sheet(
            "Detailed Comparison"
        )

        sheet2.append([

            "V1 Parameter",

            "Matched V2 Parameter",

            "Similarity",

            "Removed From V1",

            "Added In V2",

            "Comment"

        ])

        for row in comparison_results:

            sheet2.append([

                row["V1 Parameter"],

                row["V2 Parameter"],

                row["Parameter Confidence"],

                row["Removed"],

                row["Added"],

                row["Comment"]

            ])

        # =====================================
        # SHEET 3
        # BUSINESS IMPACT
        # =====================================

        sheet3 = workbook.create_sheet(
            "Business Impact"
        )

        sheet3.append([

            "Parameter",

            "Change Summary",

            "Business Impact",

            "Teams To Review",

            "Risk Level"

        ])

        for row in impact_results:

            sheet3.append([

                row["Parameter"],

                row["Change Summary"],

                row["Business Impact"],

                row["Teams"],

                row["Risk"]

            ])

        # =====================================
        # SHEET 4
        # UAT RECOMMENDATIONS
        # =====================================

        sheet4 = workbook.create_sheet(
            "UAT Recommendations"
        )

        sheet4.append([

            "Parameter",

            "Suggested Test Scenario"

        ])

        for row in impact_results:

            sheet4.append([

                row["Parameter"],

                row["UAT"]

            ])

        # =====================================
        # SHEET 5
        # AI UNDERSTANDING AUDIT
        # =====================================

        sheet5 = workbook.create_sheet(
            "AI Understanding Audit"
        )

        sheet5.append([

            "Parameter",

            "Business Area",

            "Business Understanding",

            "Key Rules",

            "Confidence"

        ])

        for row in understanding_results:

            sheet5.append([

                row["Parameter"],

                row["Business Area"],

                row["Business Understanding"],

                row["Key Rules"],

                row["Confidence"]

            ])

        # =====================================
        # AUTO FIT COLUMNS
        # =====================================

        for sheet in workbook.worksheets:

            for column in sheet.columns:

                max_length = 0

                column_letter = column[0].column_letter

                for cell in column:

                    try:

                        if cell.value:

                            max_length = max(

                                max_length,

                                len(str(cell.value))

                            )

                    except Exception:

                        pass

                adjusted_width = min(
                    max_length + 5,
                    80
                )

                sheet.column_dimensions[
                    column_letter
                ].width = adjusted_width

        # =====================================
        # SAVE FILE
        # =====================================

        workbook.save(file_name)

