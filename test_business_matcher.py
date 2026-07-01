from readers.word_reader import WordReader
from ai.archive.business_matcher import BusinessMatcher

reader = WordReader()

matcher = BusinessMatcher()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

v2 = reader.read(
    "uploads/Parameters3.docx"
)

for parameter, description in v1.items():

    result = matcher.find_match(

        parameter,

        description,

        v2

    )

    print("=" * 80)

    print("V1 Parameter:")
    print(parameter)

    print()

    print("Best Match:")
    print(result["best_match"])

    print()

    print("Confidence:")
    print(result["confidence"])

    print()

    print("Reason:")
    print(result["reason"])