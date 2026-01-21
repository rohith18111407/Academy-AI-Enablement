from unittest.mock import patch
from ingest import ingest_all

@patch("ingest.load_documents")
@patch("ingest.get_embedding")
@patch("ingest.add_to_store")
def test_ingest_pipeline(mock_add, mock_embed, mock_load):
    mock_load.return_value = ["hello world"]
    mock_embed.return_value = [0.1, 0.2]

    ingest_all()

    assert mock_add.called
