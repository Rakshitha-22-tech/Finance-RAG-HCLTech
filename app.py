import streamlit as st
from src.rag import search_documents, generate_answer


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HCLTech Finance RAG",
    page_icon="📊",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title("📊 HCLTech Finance RAG")

st.write(
    "Ask questions about HCLTech FY26 quarterly financial reports."
)


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.text_input(
    "Ask a question:",
    placeholder="Example: What was HCLTech's revenue in Q4 FY26?"
)


# ============================================================
# ASK BUTTON
# ============================================================

if st.button("Ask Question"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching financial reports..."):

            results = search_documents(question)

            answer = generate_answer(
                question,
                results
            )

        # ----------------------------------------------------
        # ANSWER
        # ----------------------------------------------------

        st.subheader("Answer")

        st.write(answer)

        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        st.subheader("Sources")

        for metadata in results["metadatas"][0]:

            st.write(
                f"📄 {metadata['source']} — "
                f"Chunk {metadata['chunk_id']}"
            )