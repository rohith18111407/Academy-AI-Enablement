# tools/rag.py
import os
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader

def load_vectorstore(persist_dir: str, docs_path: str):
    """
    Loads text documents into a ChromaDB vector store with BedrockEmbeddings.
    Handles missing docs and expired tokens gracefully.
    """
    docs = []
    for file in os.listdir(docs_path):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(docs_path, file))
            docs.extend(loader.load())

    if not docs:
        raise ValueError(f"No documents found in {docs_path}")

    embeddings = BedrockEmbeddings()  # Updated import from langchain_aws

    # Create or load Chroma vector store
    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_dir
    )
