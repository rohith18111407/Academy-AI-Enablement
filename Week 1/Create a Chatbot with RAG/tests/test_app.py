from fastapi.testclient import TestClient
from app import app
from unittest.mock import patch

client = TestClient(app)

@patch("app.get_embedding")
@patch("app.query_store")
@patch("app.generate_answer")
def test_chat_endpoint(mock_llm, mock_store, mock_embed):
    mock_embed.return_value = [0.1, 0.2]
    mock_store.return_value = (["context"], ["doc1"], [0.1])
    mock_llm.return_value = "Answer from context"

    response = client.post(
        "/chat",
        json={"question": "What is policy?"}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Answer from context"
