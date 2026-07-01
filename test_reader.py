from readers.word_reader import WordReader
from comparators.diff_engine import DiffEngine

reader = WordReader()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

v2 = reader.read(
    "uploads/Parameters3.docx"
)

engine = DiffEngine()

results = engine.compare(v1, v2)

for row in results:

    print("=" * 80)

    print("Parameter:",
          row["Parameter"])

    print("Status:",
          row["Status"])

    print("\nV1:")
    print(row["V1"])

    print("\nV2:")
    print(row["V2"])

    print("\n")

    from readers.word_reader import WordReader

reader = WordReader()

v2 = reader.read(
    "uploads/Parameters3.docx"
)

for key, value in v2.items():

    print("=" * 80)

    print("PARAMETER:")
    print(repr(key))

    print("CONTENT:")
    print(repr(value))