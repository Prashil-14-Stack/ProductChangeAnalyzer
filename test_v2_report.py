from readers.word_reader import WordReader

from ai.semantic_embedding_matcher import (
    SemanticEmbeddingMatcher
)

from comparators.diff_engine import DiffEngine

from reports.excel_generator import ExcelGenerator

from ai.impact_analyzer import ImpactAnalyzer

from ai.product_understanding_engine import (
    ProductUnderstandingEngine
)

# =====================================
# INITIALIZE SERVICES
# =====================================

reader = WordReader()

matcher = SemanticEmbeddingMatcher()

engine = DiffEngine()

impact_analyzer = ImpactAnalyzer()

product_engine = ProductUnderstandingEngine()

# =====================================
# READ DOCUMENTS
# =====================================

v1 = reader.read(
    "uploads/Parameter1.docx"
)

v2 = reader.read(
    "uploads/Parameters3.docx"
)

# =====================================
# RESULT CONTAINERS
# =====================================

matching_results = []

comparison_results = []

impact_results = []

understanding_results = []

matched_v2_parameters = set()

# =====================================
# PROCESS PARAMETERS
# =====================================

for parameter in v1.keys():

    print(f"\nProcessing: {parameter}")

    old_text = v1.get(
        parameter,
        ""
    )

    ai_result = matcher.find_match(
        parameter,
        old_text,
        v2
    )

    match = ai_result["best_match"]

    if (
        match != "NO MATCH FOUND"
    ):
        matched_v2_parameters.add(
        match
    )

    score = ai_result["confidence"]

    # =====================================
    # PRODUCT UNDERSTANDING
    # =====================================

    understanding = product_engine.understand(
        parameter,
        old_text
    )

    understanding_results.append({

        "Parameter":
            parameter,

        "Business Area":
            understanding.business_area,

        "Business Understanding":
            understanding.business_understanding,

        "Key Rules":
            ", ".join(
                understanding.key_rules
            ),

        "Confidence":
            score

    })

    # =====================================
    # MATCHING RESULTS
    # =====================================

    matching_results.append({

        "V1 Parameter":
            parameter,

        "Suggested Match":
            match,

        "Confidence":
            score,

        "Business Concept":
            ai_result["business_concept"],

        "Reason":
            ai_result["reason"],

        "Review Required":
            "Yes"
            if ai_result["review_required"]
            else "No"

    })

    # =====================================
    # GET MATCHED DESCRIPTION
    # =====================================

    if (
        match != "NO MATCH FOUND"
        and
        match in v2
    ):

        new_text = v2.get(
            match,
            ""
        )

    else:

        new_text = ""

    # =====================================
    # DIFF ANALYSIS
    # =====================================

    diff = engine.compare_text(
        old_text,
        new_text
    )

    # =====================================
    # COMPARISON RESULTS
    # =====================================

    comparison_results.append({

        "V1 Parameter":
            parameter,

        "V2 Parameter":
            match,

        "Similarity":
            score,

        "V1 Description":
            old_text,

        "V2 Description":
            new_text,

        "Removed":
            diff["Removed"],

        "Added":
            diff["Added"],

        "Comment":
            (
                f"Business comparison between "
                f"'{parameter}' and "
                f"'{match}'."
            )

    })

    # =====================================
    # IMPACT ANALYSIS
    # =====================================

    impact = impact_analyzer.analyze(
        parameter,
        diff["Added"],
        diff["Removed"]
    )

    impact_results.append({

        "Parameter":
            parameter,

        "Change Summary":
            impact["Change Summary"],

        "Business Impact":
            impact["Business Impact"],

        "Teams":
            impact["Teams"],

        "Risk":
            impact["Risk"],

        "UAT":
            impact["UAT"]

    })
# =====================================
# NEW PARAMETERS IN V2
# =====================================

for v2_parameter in v2.keys():

    if (
        v2_parameter
        not in matched_v2_parameters
    ):

        matching_results.append({

            "V1 Parameter":
                "N/A",

            "Suggested Match":
                v2_parameter,

            "Confidence":
                100,

            "Business Concept":
                "New Parameter",

            "Reason":
                "Exists only in Version 2",

            "Review Required":
                "Yes"

        })

        comparison_results.append({

            "V1 Parameter":
                "N/A",

            "V2 Parameter":
                v2_parameter,

            "Similarity":
                0,

            "V1 Description":
                "",

            "V2 Description":
                v2.get(
                    v2_parameter,
                    ""
                ),

            "Removed":
                "",

            "Added":
                "New Parameter Introduced",

            "Comment":
                "Exists only in Version 2"

        })

        impact_results.append({

            "Parameter":
                v2_parameter,

            "Change Summary":
                "New parameter introduced",

            "Business Impact":
                "Business review required",

            "Teams":
                "Product, BA, QA",

            "Risk":
                "Medium",

            "UAT":
                "Validate newly introduced parameter"

        })

        understanding_results.append({

            "Parameter":
                v2_parameter,

            "Business Area":
                "New Parameter",

            "Business Understanding":
                "Exists only in Version 2",

            "Key Rules":
                "",

            "Confidence":
                100

        })
# =====================================
# SUMMARY
# =====================================

print("\n" + "=" * 60)

print(
    "MATCHING RESULTS COUNT:",
    len(matching_results)
)

print(
    "COMPARISON RESULTS COUNT:",
    len(comparison_results)
)

print(
    "IMPACT RESULTS COUNT:",
    len(impact_results)
)

print(
    "UNDERSTANDING RESULTS COUNT:",
    len(understanding_results)
)

print("=" * 60)

print("\nPARAMETERS READ FROM V1")

print("=" * 60)

for key in v1.keys():
    print(key)

print("=" * 60)

print(
    "TOTAL PARAMETERS:",
    len(v1)
)

print("=" * 60)

# =====================================
# GENERATE EXCEL
# =====================================

print("\nGenerating Excel...")

excel = ExcelGenerator()

excel.generate_report(

    matching_results,

    comparison_results,

    impact_results,

    understanding_results,

    "comparison_v4.xlsx"

)

print(
    "\ncomparison_v4.xlsx generated successfully"
)