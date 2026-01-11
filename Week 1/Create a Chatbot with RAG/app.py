from fastapi import FastAPI
from pydantic import BaseModel

from embeddings import get_embedding
from rag_store import query_store
from llm import generate_answer
from config import TOP_K

app = FastAPI(title="RAG Chat")

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat_route(q: Query):
    q_emb = get_embedding(q.question)

    if q_emb is None:
        return {"error": "Failed to generate embedding"}

    docs, ids, dists = query_store(q_emb, TOP_K)

    context = "\n---\n".join(docs)

    prompt = f"""
Use the context below to answer the question.
If the answer is not in the context, say "I don't know".

CONTEXT:
{context}

QUESTION:
{q.question}

Answer:
"""

    answer = generate_answer(prompt)

    return {
        "question": q.question,
        "answer": answer,
        "sources": list(zip(ids, dists)),
    }
