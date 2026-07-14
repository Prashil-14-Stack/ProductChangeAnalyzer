from processors.pdf_mvp_extractor import PDFMVPExtractor
import glob


pdf_files = glob.glob(

    "test_documents/*.pdf"

)

extractor = PDFMVPExtractor()

with open(

    pdf_files[0],

    "rb"

) as file:

    parameters = extractor.extract(

        file

    )

print()

print("=" * 100)

print("BUSINESS PARAMETERS")

print("=" * 100)

for parameter in parameters:

    print()

    print("-" * 80)

    print(parameter.name)

    print()

    print(parameter.value)

    print("-" * 80)