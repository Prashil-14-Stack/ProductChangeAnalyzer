from readers.word_reader import WordReader

from ai.product_understanding_engine import (
    ProductUnderstandingEngine
)

print("=" * 100)
print("PRODUCT UNDERSTANDING ENGINE")
print("=" * 100)

reader = WordReader()

engine = ProductUnderstandingEngine()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

for parameter, description in v1.items():

    understanding = engine.understand(

        parameter,

        description

    )

    print()

    print("-" * 80)

    print(
        "Parameter:",
        understanding.parameter
    )

    print(
        "Business Understanding:",
        understanding.business_understanding
    )

    print(
        "Business Area:",
        understanding.business_area
    )

    print(
        "Key Rules:",
        understanding.key_rules
    )

    print(
        "Confidence:",
        understanding.confidence
    )

print()
print("=" * 100)
print("TEST COMPLETED")
print("=" * 100)