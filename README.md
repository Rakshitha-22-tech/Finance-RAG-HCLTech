\# 📊 HCLTech Finance RAG



A Retrieval-Augmented Generation (RAG) application that allows users to ask questions about HCLTech FY26 quarterly financial reports.



The system retrieves relevant information from HCLTech's financial reports and uses Llama 3 through Ollama to generate grounded answers.



\---



\## 🎯 Project Objective



The objective of this project is to build a financial question-answering system using RAG.



Instead of asking an AI model to answer from its general knowledge, this application retrieves relevant information from HCLTech's FY26 financial reports and uses that information to generate the answer.



The system supports questions related to:



\- Revenue

\- EBIT

\- Net Income

\- Quarterly financial performance

\- QoQ growth

\- YoY growth



\---



\## 🧠 What is RAG?



RAG stands for \*\*Retrieval-Augmented Generation\*\*.



The system follows these steps:



1\. Load HCLTech financial reports.

2\. Extract text from PDF files.

3\. Split the extracted text into smaller chunks.

4\. Generate embeddings using `nomic-embed-text`.

5\. Store the embeddings in ChromaDB.

6\. Retrieve relevant chunks for a user's question.

7\. Send the retrieved context to Llama 3.

8\. Generate a grounded financial answer.

9\. Display the answer and source documents.



\---



\## 🏗️ System Architecture



```text

HCLTech FY26 PDF Reports

&#x20;         │

&#x20;         ▼

&#x20;    PDF Extraction

&#x20;         │

&#x20;         ▼

&#x20;     Text Files

&#x20;         │

&#x20;         ▼

&#x20;     Text Chunking

&#x20;         │

&#x20;         ▼

&#x20;  Nomic Text Embeddings

&#x20;         │

&#x20;         ▼

&#x20;      ChromaDB

&#x20;         │

&#x20;         ▼

&#x20;     User Question

&#x20;         │

&#x20;         ▼

&#x20;  Question Embedding

&#x20;         │

&#x20;         ▼

&#x20;Relevant Document Chunks

&#x20;         │

&#x20;         ▼

&#x20;      Llama 3

&#x20;         │

&#x20;         ▼

&#x20;   Financial Answer

&#x20;         │

&#x20;         ▼

&#x20;     Source Chunks

