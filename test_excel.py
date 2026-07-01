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

results = []

for parameter in v1.keys():

    match, score = matcher.find_match(
        parameter,
        v2.keys()
    )

    results.append({
        "Parameter": parameter,
        "Best Match": match,
        "Similarity": score
    })

excel = ExcelGenerator()

excel.generate(
    results,
    "comparison_report.xlsx"
)

print("Excel Report Generated")