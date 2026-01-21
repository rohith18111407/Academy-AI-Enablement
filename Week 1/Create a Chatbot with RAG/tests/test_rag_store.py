from rag_store import add_to_store, query_store
import chromadb
import tempfile

def test_add_and_query_store(monkeypatch):
    temp_dir = tempfile.mkdtemp()

    client = chromadb.PersistentClient(path=temp_dir)
    collection = client.get_or_create_collection("test")

    monkeypatch.setattr("rag_store.collection", collection)

    add_to_store("doc1", "hello world", [0.1, 0.2])
    docs, ids, dists = query_store([0.1, 0.2], top_k=1)

    assert docs[0] == "hello world"
    assert ids[0] == "doc1"
