from pathlib import Path
import chromadb
import ollama

DATA_DIR = Path("data")
CHROMA_DIR = Path("chroma_db")

# Connect to local ChromaDB
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name="finance_documents"
)

# Read chunks
chunks_file = DATA_DIR / "chunks.txt"
text = chunks_file.read_text(encoding="utf-8")

# Split chunks using the separator created earlier
raw_chunks = [
    chunk.strip()
    for chunk in text.split("-" * 80)
    if chunk.strip()
]

documents = []
ids = []
metadatas = []
embeddings = []

for i, chunk in enumerate(raw_chunks):
    lines = chunk.splitlines()

    source = "unknown"
    chunk_id = str(i)

    for line in lines:
        if line.startswith("SOURCE:"):
            source = line.replace("SOURCE:", "").strip()
        elif line.startswith("CHUNK_ID:"):
            chunk_id = line.replace("CHUNK_ID:", "").strip()

    # Remove metadata lines from the actual document text
    document_text = "\n".join(
        line for line in lines
        if not line.startswith("SOURCE:")
        and not line.startswith("CHUNK_ID:")
    ).strip()

    if not document_text:
        continue

    # Generate embedding using local Ollama
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=document_text
    )

    documents.append(document_text)
    ids.append(f"{source}_{chunk_id}")
    metadatas.append({
        "source": source,
        "chunk_id": chunk_id
    })
    embeddings.append(response["embedding"])

    print(f"Embedded {len(documents)}/{len(raw_chunks)}")

# Store everything in ChromaDB
if documents:
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

print("\n" + "=" * 50)
print("VECTOR DATABASE CREATED SUCCESSFULLY")
print("=" * 50)
print(f"Documents stored: {collection.count()}")
print(f"Database location: {CHROMA_DIR}")