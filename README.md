# llm-local-chat
A simple chat application using Lang-Chain and RAG approach using llama3 

# Overview

Mastodon-GPT is a university-focused chatbot that integrates Large Language Models (LLMs) with LangChain and Retrieval-Augmented Generation (RAG).

It automatically fetches and processes university web content and uploaded documents, stores them in a vector database (FAISS), and allows students or visitors to query the system through a chatbot interface. Responses are context-aware and grounded in the latest available university information.

Admins can easily manage knowledge sources (links/documents) via a secure dashboard, while students benefit from an AI-powered Q&A experience.

# Features
🔹 User Features

Interactive chatbot integrated into university web pages.

Context-aware responses based on university documents & links.

Ability to clear chat history within sessions.

🔹 Admin Features

Secure login with role-based access control.

Upload/remove web URLs and documents to enrich chatbot knowledge.

Dashboard for managing content sources.

🔹 System Features

Automated content pipeline: Scheduled Python script fetches and chunks university data weekly.

Semantic search with embeddings stored in FAISS.

LLM integration (Gemini) for generating context-aware answers.

Context persistence for handling follow-up questions.

#  Architecture

Backend: Python (Flask/FastAPI)

Database: PostgreSQL (metadata + admin details)

Vector DB: FAISS (semantic search)

Frameworks & Models:

LangChain → RAG pipeline

SentenceTransformer (paraphrase-multilingual) → Embeddings

Gemini-2.0-flash-thinking-exp-01-21 → LLM response generation

# Workflow:

Admin uploads links/docs → processed → chunked → embedded → stored in FAISS.

Scheduler updates knowledge base weekly.

User asks a query → embedding model retrieves relevant context.

Context + query passed to LLM → response generated.

## Ollama setup and Installation
```bash
download and install : https://ollama.com/download
```
## Pull llama3 and paraphrase-multilingual model
```bash 
ollama pull llama3
ollama pull paraphrase-multilingual-MiniLM-L12-v2
```
## Install postgres DB and create a database with the tables below
```sql
CREATE TABLE link_t (
    id integer PRIMARY KEY,
    value TEXT NOT NULL,
    type TEXT NOT NULL,
    createtimestamp TIMESTAMP without time zone DEFAULT CURRENT_TIMESTAMP,
    updatetimestamp TIMESTAMP without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT link_t_type_check CHECK (type IN ('web_url', 'file_path')) 
);


CREATE TABLE Chat_Audit (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    create_time TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE Admin_data (
    id SERIAL PRIMARY KEY, --  Unique identifier for admin data
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email_id VARCHAR(255) UNIQUE NOT NULL, -- Unique email for admin
    user_name VARCHAR(100) UNIQUE NOT NULL, -- Unique username for admin
    password VARCHAR(255) NOT NULL, -- Hashed password
    last_login TIMESTAMP, -- Last login timestamp
    create_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);
```

## To install all required dependencies
```bash
pip install -r requirements.txt
```
## To refresh the app with new dependencies
```bash
poetry lock
poetry update
poetry sync
```
Update the poetry.lock and pyproject.toml files to include any other dependencies if needed

## To build
```bash 
poetry build
```
## To run the application locally using waitress after installing whl file
```bash
waitress-serve --port=5000 llmchat.app:app
```

## To run the application from an IDE
```bash 
app.py
```

Once the application is up and running, access using localhost:5000
