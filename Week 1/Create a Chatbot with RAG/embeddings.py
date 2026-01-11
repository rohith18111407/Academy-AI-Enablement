import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"

def get_embedding(text: str):
    if not text or not text.strip():
        return None

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBED_MODEL,
            "prompt": text
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    embedding = data.get("embedding")

    # 🔐 CRITICAL SAFETY CHECK
    if embedding is None or len(embedding) == 0:
        return None

    return embedding
