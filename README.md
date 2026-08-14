# 📊 HCLTech Finance RAG

A Retrieval-Augmented Generation (RAG) application that allows users to ask questions about HCLTech FY26 quarterly financial reports and receive grounded answers based on the available financial documents.

The application combines document retrieval, vector embeddings, ChromaDB, Ollama, Llama 3, and Streamlit to create a local financial question-answering system.

## 🎯 Project Objective

The objective of this project is to build a financial question-answering application using Retrieval-Augmented Generation (RAG).

Instead of relying only on the general knowledge of an AI model, the system first retrieves relevant information from HCLTech FY26 financial reports and then provides that information as context to the language model.

This helps the system generate answers that are grounded in the provided financial documents.

## 💡 Key Features

- Ask natural-language questions about HCLTech financial reports
- Retrieve relevant financial information using semantic search
- Generate embeddings using `nomic-embed-text`
- Store and search document embeddings using ChromaDB
- Generate grounded responses using Llama 3
- Run the LLM locally using Ollama
- Interactive Streamlit web interface
- Display relevant source information along with answers
- Supports questions related to revenue, EBIT, net income, quarterly performance, QoQ growth, and YoY growth

## 🧠 What is RAG?

RAG stands for **Retrieval-Augmented Generation**.

It combines information retrieval with a Large Language Model.

### RAG Workflow

1. Load HCLTech financial reports.
2. Extract text from the documents.
3. Split the extracted text into smaller chunks.
4. Generate embeddings using `nomic-embed-text`.
5. Store the embeddings in ChromaDB.
6. Convert the user's question into an embedding.
7. Retrieve the most relevant document chunks.
8. Provide the retrieved context to Llama 3.
9. Generate a grounded financial answer.
10. Display the answer and relevant source information.

## 🏗️ System Architecture

```text
HCLTech FY26 Financial Reports
            │
            ▼
      PDF Text Extraction
            │
            ▼
        Text Chunking
            │
            ▼
   Nomic Text Embeddings
            │
            ▼
         ChromaDB
            │
            │
      User Question
            │
            ▼
    Question Embedding
            │
            ▼
   Relevant Document Chunks
            │
            ▼
          Llama 3
            │
            ▼
     Grounded Answer
            │
            ▼
     Streamlit Interface
🛠️ Technologies Used
Technology	Purpose
Python	Application and RAG pipeline
ChromaDB	Vector database and similarity search
Ollama	Local AI model execution
Llama 3	Financial answer generation
Nomic Embed Text	Document and question embeddings
Streamlit	Web application interface
PyPDF	PDF text extraction

Finance-RAG-HCLTech/
│
├── data/
│   └── Financial report data
│
├── src/
│   ├── extract_text.py
│   ├── chunk_text.py
│   ├── create_vector_db.py
│   └── rag.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore

🔐 Grounded Responses

The application is designed to answer questions using the retrieved financial document context rather than relying on unrelated external knowledge.

This helps reduce the possibility of generating unsupported financial figures.

👩‍💻 My Implementation

This project was implemented, configured, tested, and deployed as part of the HCLTech Campus Ambassador learning task.

Work Completed
Set up the Python-based RAG environment
Configured Ollama for local AI model execution
Set up nomic-embed-text for embeddings
Created the ChromaDB vector database
Configured the RAG retrieval pipeline
Configured Llama 3 for answer generation
Tested financial question answering
Ran the application using Streamlit
Verified the complete workflow from user question to generated answer
Published the project on GitHub
📚 Learning Outcomes
Through this project, I gained practical experience with:

Retrieval-Augmented Generation (RAG)
Large Language Models
Vector databases
Text embeddings
Semantic search
Context-based prompt generation
Local AI models using Ollama
Streamlit application development
Git and GitHub
Building an end-to-end AI application
🔮 Future Improvements

Possible future enhancements include:

Improved financial dashboard
Better source citation and document references
Comparison of multiple quarters
Interactive financial charts
Conversation history
Support for additional financial reports
Improved error handling for unrelated questions
Downloadable financial analysis reports
👤 Author

Rakshitha

GitHub: https://github.com/Rakshitha-22-tech
📌 Project Status

Completed and tested successfully.

The current implementation supports document retrieval, embedding generation, vector search, Llama 3-based answer generation, and a Streamlit interface for asking questions about HCLTech financial reports.




#
