from readers.word_reader import WordReader
from reports.excel_generator import ExcelGenerator

reader = WordReader()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

v2 = reader.read(
    "uploads/Parameters3.docx"
)

all_parameters = set(v1.keys()) | set(v2.keys())

results = []

for parameter in all_parameters:

    old_value = v1.get(parameter, "")

    new_value = v2.get(parameter, "")

    if parameter not in v1:

        status = "Added"

    elif parameter not in v2:

        status = "Removed"

    elif old_value == new_value:

        status = "No Change"

    else:

        status = "Modified"

    results.append({
        "Parameter": parameter,
        "Status": status,
        "V1": old_value,
        "V2": new_value
    })

excel = ExcelGenerator()

excel.generate(
    results,
    "comparison_report.xlsx"
)

print("Comparison Report Generated")