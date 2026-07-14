import fitz
import json
import glob


pdf_files = glob.glob("test_documents/*.pdf")

if not pdf_files:
    raise FileNotFoundError(
        "No PDF found inside test_documents/"
    )

pdf_path = pdf_files[0]

print(f"Reading: {pdf_path}")

pdf = fitz.open(pdf_path)

page = pdf.load_page(0)

raw = page.get_text("rawdict")

output_file = "rawdict_page1.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(raw, f, indent=4)

pdf.close()

print(f"\n✅ RAWDICT exported to {output_file}")