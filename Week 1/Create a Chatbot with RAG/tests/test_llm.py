from unittest.mock import patch
from llm import generate_answer

@patch("llm.requests.post")
def test_generate_answer(mock_post):
    mock_post.return_value.json.return_value = {
        "response": "This is the answer"
    }
    mock_post.return_value.raise_for_status = lambda: None

    answer = generate_answer("test prompt")
    assert answer == "This is the answer"
