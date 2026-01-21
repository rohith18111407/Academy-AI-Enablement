from utils import chunk_text

def test_chunk_text_basic():
    text = "a" * 1000
    chunks = chunk_text(text, chunk_size=200, overlap=50)

    assert len(chunks) > 1
    assert all(len(c) <= 200 for c in chunks)
