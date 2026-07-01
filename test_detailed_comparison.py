from readers.word_reader import WordReader
from extractors.paramater_matcher import ParameterMatcher
from comparators.diff_engine import DiffEngine

reader = WordReader()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

v2 = reader.read(
    "uploads/Parameters3.docx"
)

matcher = ParameterMatcher()

engine = DiffEngine()

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

    result = engine.compare_text(
        old_text,
        new_text
    )

    print("=" * 80)

    print("Parameter:")
    print(parameter)

    print("\nMatched With:")
    print(match)

    print("\nAdded:")
    print(result["Added"])

    print("\nRemoved:")
    print(result["Removed"])