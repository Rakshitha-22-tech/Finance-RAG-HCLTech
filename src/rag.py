import re
import chromadb
import ollama


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "finance_documents"

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3:latest"


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = client.get_collection(
    name=COLLECTION_NAME
)


# ============================================================
# DETECT QUARTER
# ============================================================

def detect_quarter(question):
    """
    Detect Q1, Q2, Q3 or Q4 from the question.
    """

    match = re.search(
        r"\b(Q[1-4])\s*(?:FY)?26\b",
        question.upper()
    )

    if match:
        return match.group(1)

    return None


# ============================================================
# IDENTIFY QUESTION TYPE
# ============================================================

def detect_question_type(question):
    """
    Identify whether the question is about revenue,
    EBIT, or net income.
    """

    q = question.lower()

    if "revenue" in q:
        return "revenue"

    if "ebit" in q:
        return "ebit"

    if (
        "net income" in q
        or "net profit" in q
        or re.search(r"\bni\b", q)
    ):
        return "net_income"

    return "general"


# ============================================================
# SEARCH DOCUMENTS
# ============================================================

def search_documents(question, top_k=5):
    """
    Retrieve the best financial chunks.

    For a specific quarter, only that quarter's report
    is considered.

    For financial questions, explicit quarterly highlights
    are strongly preferred over annual figures.
    """

    quarter = detect_quarter(question)
    question_type = detect_question_type(question)

    # --------------------------------------------------------
    # Create question embedding
    # --------------------------------------------------------

    response = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=question
    )

    # --------------------------------------------------------
    # Search all chunks
    # --------------------------------------------------------

    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=244
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    candidates = []

    # --------------------------------------------------------
    # Score every chunk
    # --------------------------------------------------------

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        source = metadata["source"].upper()
        text = document.lower()

        # ----------------------------------------------------
        # QUARTER FILTER
        # ----------------------------------------------------

        if quarter:

            expected_source = f"HCLTECH_{quarter}_FY26.TXT"

            if expected_source not in source:
                continue

        score = 0

        # ----------------------------------------------------
        # GENERAL RELEVANCE
        # ----------------------------------------------------

        if "revenue" in text:
            score += 10

        if "qoq" in text:
            score += 10

        if "yoy" in text:
            score += 10

        # ----------------------------------------------------
        # QUARTERLY FINANCIAL HIGHLIGHTS
        # ----------------------------------------------------

        # This is extremely important because the quarterly
        # highlights contain the exact quarter figures.

        if "qoq" in text and "yoy" in text:
            score += 100

        if "profitability & return metrics" in text:
            score += 100

        # ----------------------------------------------------
        # REVENUE QUESTION
        # ----------------------------------------------------

        if question_type == "revenue":

            if "inr revenue of" in text:
                score += 500

            if "revenue of" in text:
                score += 200

            # Explicit quarterly growth
            if "qoq" in text and "yoy" in text:
                score += 100

        # ----------------------------------------------------
        # EBIT QUESTION
        # ----------------------------------------------------

        elif question_type == "ebit":

            if "inr ebit at" in text:
                score += 500

            if "ebit at" in text:
                score += 200

            if "profitability & return metrics" in text:
                score += 100

        # ----------------------------------------------------
        # NET INCOME QUESTION
        # ----------------------------------------------------

        elif question_type == "net_income":

            # Exact quarterly statement:
            # NI at ₹4,488 Crores ...
            if "ni at" in text:
                score += 500

            # Net Income wording
            if "net income" in text:
                score += 200

            # Quarterly growth makes it much more likely
            # to be the requested quarter rather than FY26.
            if "qoq" in text and "yoy" in text:
                score += 300

            if "profitability & return metrics" in text:
                score += 150

            # Annual-only wording gets penalized.
            if "for the year" in text:
                score -= 300

            if "fy26 results" in text:
                score -= 300

        # ----------------------------------------------------
        # PENALIZE ANNUAL-ONLY FINANCIAL FIGURES
        # ----------------------------------------------------

        if quarter:

            if "for the year came in" in text:
                score -= 300

            if "for the year" in text:
                score -= 200

            if "fy26 results" in text:
                score -= 200

        # ----------------------------------------------------
        # COMBINE WITH SEMANTIC DISTANCE
        # ----------------------------------------------------

        final_score = score - distance

        candidates.append(
            (
                final_score,
                document,
                metadata,
                distance
            )
        )

    # --------------------------------------------------------
    # SORT BEST RESULTS
    # --------------------------------------------------------

    candidates.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # --------------------------------------------------------
    # SELECT TOP RESULTS
    # --------------------------------------------------------

    selected = candidates[:top_k]

    return {
        "documents": [
            [item[1] for item in selected]
        ],
        "metadatas": [
            [item[2] for item in selected]
        ],
        "distances": [
            [item[3] for item in selected]
        ]
    }


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, results):
    """
    Generate an answer using ONLY retrieved context.
    """

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not documents:
        return (
            "I could not find this information in the "
            "provided financial reports."
        )

    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context_parts = []

    for i, document in enumerate(documents):

        source = metadatas[i]["source"]
        chunk_id = metadatas[i]["chunk_id"]

        context_parts.append(
            f"[Source: {source}, Chunk: {chunk_id}]\n"
            f"{document}"
        )

    context = "\n\n".join(context_parts)

    # --------------------------------------------------------
    # STRICT FINANCIAL PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are a financial research assistant for HCLTech.

Answer the question using ONLY the CONTEXT.

STRICT RULES:

1. Do not use outside knowledge.

2. Do not invent any number.

3. Do not calculate or estimate financial figures.

4. NEVER divide annual revenue by 4.

5. If the question asks about a specific quarter,
   use the quarterly figure for that quarter.

6. Do not use the annual FY26 figure when the question
   asks for quarterly Q1, Q2, Q3, or Q4 information.

7. For Revenue questions, prefer:
   "INR Revenue of ..."

8. For EBIT questions, prefer:
   "INR EBIT at ..."

9. For Net Income questions, prefer:
   "NI at ..."

10. If a quarterly figure contains QoQ and YoY information,
    prefer that figure over an annual figure.

11. Give ONLY the answer requested.

12. Do not repeat the question.

13. Mention the source report and chunk.

14. If the exact answer is not available, say:

"I could not find this information in the provided
financial reports."

QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    return response["message"]["content"]


# ============================================================
# ASK QUESTION
# ============================================================

def ask_question(question):

    results = search_documents(question)

    answer = generate_answer(
        question,
        results
    )

    print("\n" + "=" * 70)
    print("QUESTION")
    print("=" * 70)
    print(question)

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(answer)

    print("\n" + "=" * 70)
    print("SOURCES")
    print("=" * 70)

    for metadata in results["metadatas"][0]:

        print(
            f"- {metadata['source']} | "
            f"Chunk {metadata['chunk_id']}"
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    question = input(
        "\nAsk a question about HCLTech's financial reports: "
    )

    ask_question(question)