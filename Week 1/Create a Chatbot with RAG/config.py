import os
from dotenv import load_dotenv
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
EMBED_MODEL = os.getenv("EMBED_MODEL")
LLM_MODEL = os.getenv("LLM_MODEL")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "rag_docs")
TOP_K = int(os.getenv("TOP_K", "5"))
