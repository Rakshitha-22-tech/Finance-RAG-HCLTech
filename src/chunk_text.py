from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = Path("data")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

all_chunks = []

for txt_file in sorted(DATA_DIR.glob("*.txt")):
    print(f"\nProcessing: {txt_file.name}")

    text = txt_file.read_text(encoding="utf-8")
    chunks = splitter.split_text(text)

    print(f"Characters: {len(text)}")
    print(f"Chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "source": txt_file.name,
            "chunk_id": i,
            "text": chunk
        })

print("\n" + "=" * 50)
print(f"TOTAL CHUNKS: {len(all_chunks)}")
print("=" * 50)

output_file = DATA_DIR / "chunks.txt"

with output_file.open("w", encoding="utf-8") as f:
    for item in all_chunks:
        f.write(f"SOURCE: {item['source']}\n")
        f.write(f"CHUNK_ID: {item['chunk_id']}\n")
        f.write(item["text"])
        f.write("\n" + "-" * 80 + "\n")

print(f"Saved chunks to: {output_file}")