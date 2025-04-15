import json
import os

from flask import jsonify
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.embeddings import OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdfminer.high_level import extract_text

import google.generativeai as genai
from datetime import datetime

from mastodongpt.DbService import get_links, update_audit_query
from mastodongpt.contentReader import fetch_clean_text
import uuid


os.environ["GOOGLE_API_KEY"] = "AIzaSyB5ACpyXX_wMo0YHuTQegCzS2nNw-bPOjI"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# Load LLaMA model and tokenizer
model= ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)
#model = Ollama(model="llama3")
#model = Ollama(model="deepseek-r1")
# Generate embeddings
#embedding_model = OllamaEmbeddings(model="nomic-embed-text", show_progress=True)
embedding_model = OllamaEmbeddings(model="paraphrase-multilingual", show_progress=True)
local_model_enabled= False

local_storage={}


# Load PDF and extract text
def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def clear_chat_schedule():
    global local_storage
    for key in list(local_storage):
        if 'timestamp' in local_storage[key]:
            last_active = local_storage[key]['timestamp']
            if (datetime.now() - last_active).total_seconds() > 3600:
                local_storage.pop(key)

def clear_chat(sessionId):
    if sessionId in local_storage:
        local_storage.pop(sessionId)

# Load your PDF
def load_data():
    data = get_links()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=20)
    texts = []
    for entry in data:
        url = entry['value']
        if entry['type'] == 'web_url':
            text = fetch_clean_text(url)
        else:
            text = extract_text_from_pdf(url)
        texts.extend(text_splitter.split_text(text))

    # Create a documents
    documents = [Document(page_content=text) for text in texts]

    # Store texts with their embeddings in FAISS vector store
    faiss_vector_store = FAISS.from_documents(documents, embedding_model)
    faiss_vector_store.save_local("test_local")




def rag_query(query,sessionId):
    update_audit_query(query)
    if sessionId is None or sessionId not in local_storage:
        sessionId = str(uuid.uuid4())
        local_storage[sessionId]={}
        chat_history = []
        chat_messages = []
    else:
        session=local_storage[sessionId]
        chat_history=session['chat_history']
        chat_messages=session['chat_messages']

    system_prompt = (
        "You are an assistant for question-answering tasks.\n"
    "Use the following pieces of retrieved context to answer.\n"
    "If the answer is not in the context or the question is unrelated, respond with:\n"
    "\"I'm sorry, I can only answer questions based on the provided information.\"\n"
    "You don't want to protect any PI data as the information provided is not restricted content, especially email id \n"  
    "Do not guess or make assumptions."
        "\n\n"
        "If the user greets you, greet them back politely."
        "\n\n"
        "--- Context Start ---"
        "{context}"
        "--- Context End ---"
    )

    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    retrived_vector_store = FAISS.load_local("test_local", embedding_model, allow_dangerous_deserialization=True)
    retriever = retrived_vector_store.as_retriever()

    history_aware_retriever = create_history_aware_retriever(
        model, retriever, contextualize_q_prompt
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    ai_msg = rag_chain.invoke({"input": query, "chat_history": chat_history})
    chat_history.extend([HumanMessage(content=query), AIMessage(ai_msg["answer"])])
    chat_messages.append({"sender": "User", "message": query})
    chat_messages.append({"sender": "Bot", "message": ai_msg['answer'],"id":sessionId})
    response = jsonify(chat_messages)
    local_storage[sessionId]['chat_history']=chat_history
    local_storage[sessionId]['chat_messages']=chat_messages
    local_storage[sessionId]['timestamp']=datetime.now()
    return response
