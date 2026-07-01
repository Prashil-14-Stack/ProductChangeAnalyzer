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

    print("=" * 50)

    print("Parameter:",
          row["Parameter"])

    print("Status:",
          row["Status"])