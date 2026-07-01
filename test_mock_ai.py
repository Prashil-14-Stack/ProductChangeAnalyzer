from readers.word_reader import WordReader
from ai.mock_ai_matcher import MockAIMatcher

reader = WordReader()

matcher = MockAIMatcher()

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

    print("Parameter:")
    print(parameter)

    print()

    print(result)