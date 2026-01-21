import os
from document_loaders import load_txt, clean_text

def test_load_txt(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("Hello World")

    text = load_txt(str(file))
    assert text == "Hello World"

def test_clean_text():
    raw = "Hello\x00 World "
    assert clean_text(raw) == "Hello World"
