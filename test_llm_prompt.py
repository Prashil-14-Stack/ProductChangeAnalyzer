from readers.word_reader import WordReader

from ai.llm_product_understanding import (
    LLMProductUnderstanding
)

from processors.parameter_cleaner import (
    ParameterCleaner
)

print("=" * 100)
print("LLM PRODUCT UNDERSTANDING TEST")
print("=" * 100)

reader = WordReader()

engine = LLMProductUnderstanding()

cleaner = ParameterCleaner()

v1 = reader.read(
    "uploads/Parameter1.docx"
)

valid_parameter_count = 0

for parameter, description in v1.items():

    if not cleaner.is_valid_parameter(
            parameter,
            description):

        print(
            f"Skipping Non-Business Parameter: "
            f"{parameter}"
        )

        continue

    valid_parameter_count += 1

    prompt = engine.build_prompt(

        parameter,

        description

    )

    print()

    print("=" * 100)

    print(
        f"BUSINESS PARAMETER "
        f"#{valid_parameter_count}"
    )

    print("=" * 100)

    print(prompt)

    print()

    print("-" * 100)

    # Show first 5 parameters only
    # for demo purposes

    if valid_parameter_count >= 5:

        break

print()

print("=" * 100)
print(
    f"Total Business Parameters Processed: "
    f"{valid_parameter_count}"
)
print("=" * 100)