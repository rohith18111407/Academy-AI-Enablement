from document_loaders import load_documents
from utils import chunk_text
from embeddings import get_embedding
from rag_store import add_to_store

def ingest_all():
    docs = load_documents("documents")

    for idx, doc in enumerate(docs):
        chunks = chunk_text(doc)

        for j, chunk in enumerate(chunks):
            emb = get_embedding(chunk)

            # 🔐 SAFETY CHECK
            if emb is None:
                print(f"⚠️ Skipping empty embedding (doc {idx}, chunk {j})")
                continue

            add_to_store(
                f"doc_{idx}_{j}",
                chunk,
                emb
            )
    print(f"📄 Loaded {len(docs)} documents")            

if __name__ == "__main__":
    ingest_all()
