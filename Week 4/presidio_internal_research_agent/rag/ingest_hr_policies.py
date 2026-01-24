from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from config.settings import (
    HR_POLICY_PATH,
    CHROMA_DB_PATH,
    EMBEDDING_MODEL
)


def ingest_hr_policies():
    """
    Loads HR policy documents, splits them into chunks,
    generates embeddings, and stores them in ChromaDB.
    """

    loader = DirectoryLoader(
        HR_POLICY_PATH,
        glob="**/*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )

    print("HR policy documents indexed successfully in ChromaDB")


if __name__ == "__main__":
    ingest_hr_policies()

# ppython3 -m rag.ingest_hr_policies
    
