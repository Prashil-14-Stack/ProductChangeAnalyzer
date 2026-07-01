from readers.word_reader import WordReader
from extractors.paramater_matcher import ParameterMatcher
from comparators.diff_engine import DiffEngine
from reports.excel_generator import ExcelGenerator

reader = WordReader()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

v2 = reader.read(
    "uploads/Parameters3.docx"
)

matcher = ParameterMatcher()

engine = DiffEngine()

results = []

for parameter in v1.keys():

    match, score = matcher.find_match(
        parameter,
        v2.keys()
    )

    if score < 70:

        continue

    old_text = v1.get(
        parameter,
        ""
    )

    new_text = v2.get(
        match,
        ""
    )

    diff = engine.compare_text(
        old_text,
        new_text
    )

    results.append({

        "V1 Parameter":
            parameter,

        "V2 Parameter":
            match,

        "Similarity":
            round(score, 2),

        "Added":
            diff["Added"],

        "Removed":
            diff["Removed"]

    })

excel = ExcelGenerator()

excel.generate_detailed_report(

    results,

    "detailed_comparison.xlsx"

)

print(
    "Detailed Comparison Report Generated"
)