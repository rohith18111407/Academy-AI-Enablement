from langchain_core.messages import HumanMessage

def is_answerable(llm, context: str, question: str) -> bool:
    """
    Uses LLM to determine whether the context contains enough
    information to answer the question.
    """
    prompt = f"""
Answer ONLY with YES or NO.

Can the following question be answered using ONLY the context below?

Context:
{context}

Question:
{question}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip().upper() == "YES"
