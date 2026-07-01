from readers.word_reader import WordReader
from extractors.paramater_matcher import ParameterMatcher
from reports.excel_generator import ExcelGenerator

reader = WordReader()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

v2 = reader.read(
    "uploads/Parameters3.docx"
)

matcher = ParameterMatcher()

matching_results = []

analysis_results = []

for parameter in v1.keys():

    match, score = matcher.find_match(
        parameter,
        v2.keys()
    )

    # ----------------------------
    # Matching Sheet
    # ----------------------------

    if score >= 85:

        review_required = "No"

    elif score >= 70:

        review_required = "Medium"

    else:

        review_required = "Yes"

    matching_results.append({

        "V1 Parameter": parameter,

        "V2 Parameter": match,

        "Similarity": round(score, 2),

        "Status": "Modified",

        "Review Required":
            review_required
    })

    # ----------------------------
    # Analysis Sheet
    # ----------------------------

    analysis_results.append({

        "Parameter": parameter,

        "Change Summary":
            "Comparison identified. Review required.",

        "Business Impact":
            "To Be Determined",

        "Teams To Review":
            "Product, UAT",

        "UAT Recommendation":
            "Review business rules and create test scenarios"
    })

excel = ExcelGenerator()

excel.generate(
    matching_results,
    analysis_results,
    "final_comparison_report.xlsx"
)

print(
    "Final Comparison Report Generated"
)