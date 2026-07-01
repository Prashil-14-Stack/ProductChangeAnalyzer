from readers.word_reader import WordReader
from extractors.paramater_matcher import ParameterMatcher

reader = WordReader()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

v2 = reader.read(
    "uploads/Parameters3.docx"
)

matcher = ParameterMatcher()

for parameter in v1.keys():

    match, score = matcher.find_match(
        parameter,
        v2.keys()
    )

    print("=" * 60)

    print("V1 Parameter:")
    print(parameter)

    print("\nBest Match:")
    print(match)

    print("\nSimilarity:")
    print(score)