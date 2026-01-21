from unittest.mock import patch
from embeddings import get_embedding

@patch("embeddings.requests.post")
def test_get_embedding(mock_post):
    mock_post.return_value.json.return_value = {
        "embedding": [0.1, 0.2, 0.3]
    }
    mock_post.return_value.raise_for_status = lambda: None

    emb = get_embedding("hello")
    assert emb == [0.1, 0.2, 0.3]

def test_get_embedding_empty():
    assert get_embedding("") is None
