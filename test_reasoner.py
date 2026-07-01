from readers.word_reader import WordReader
from ai.business_reasoner import BusinessReasoner

print("Starting test...")

reader = WordReader()

reasoner = BusinessReasoner()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

print("Parameters found:", len(v1))

for parameter, description in v1.items():

    concept = reasoner.classify(
        parameter,
        description
    )

    print(
        parameter,
        "=>",
        concept
    )

print("Finished.")