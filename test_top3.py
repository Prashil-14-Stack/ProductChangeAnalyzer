from readers.word_reader import WordReader
from ai.semantic_embedding_matcher import (
    SemanticEmbeddingMatcher
)

reader = WordReader()

matcher = SemanticEmbeddingMatcher()

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

    print("Top 3 Matches:")

    for candidate in result["top_matches"]:

        print(candidate)

    print()