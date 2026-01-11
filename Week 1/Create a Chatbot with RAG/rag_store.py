import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="rag_docs"
)

def add_to_store(doc_id, text, embedding):
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding]
    )

def query_store(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return (
        results.get("documents", [[]])[0],
        results.get("ids", [[]])[0],
        results.get("distances", [[]])[0],
    )
