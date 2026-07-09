from pathlib import Path

from readers.pdf_reader import PDFReader

sample_folder = Path("samples")

pdf_files = list(sample_folder.glob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError("No PDF found inside samples folder.")

pdf_path = pdf_files[0]

print(f"Reading: {pdf_path.name}")

reader = PDFReader()

document = reader.read(pdf_path)

print(document.summary())

print()

print(document.text[:1000])