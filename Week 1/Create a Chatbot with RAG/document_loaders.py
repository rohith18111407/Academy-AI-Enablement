import os
from pypdf import PdfReader
from docx import Document

def load_txt(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read()

def load_pdf(path):
    text = ""
    pdf = PdfReader(path)
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text

def load_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def load_documents(folder="documents"):
    docs = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if file.lower().endswith(".pdf"):
            docs.append(load_pdf(path))
        elif file.lower().endswith(".docx"):
            docs.append(load_docx(path))
        elif file.lower().endswith(".txt"):
            docs.append(load_txt(path))
    return docs

def clean_text(text: str) -> str:
    return text.replace("\x00", "").strip()

