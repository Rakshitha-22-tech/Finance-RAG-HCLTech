from pathlib import Path
from pypdf import PdfReader

DATA_DIR = Path("data")

for pdf_file in sorted(DATA_DIR.glob("*.pdf")):
    print(f"\n{'=' * 60}")
    print(f"FILE: {pdf_file.name}")
    print(f"{'=' * 60}")

    reader = PdfReader(str(pdf_file))

    print(f"Pages: {len(reader.pages)}")

    text = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    print(f"Characters extracted: {len(text)}")

    output_file = pdf_file.with_suffix(".txt")
    output_file.write_text(text, encoding="utf-8")

    print(f"Saved: {output_file}")