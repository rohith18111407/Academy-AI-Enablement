from langchain.tools import Tool
from rag.chroma_store import get_chroma_retriever


def hr_policy_search(query: str) -> str:
    retriever = get_chroma_retriever()
    docs = retriever.get_relevant_documents(query)

    if not docs:
        return "No relevant internal HR policy information found."

    return "\n\n".join(
        f"{doc.page_content}"
        for doc in docs
    )


def get_hr_policy_rag_tool():
    return Tool(
        name="HR_Policy_RAG",
        func=hr_policy_search,
        description=(
            "Use this tool for questions related to Presidio internal HR policies, "
            "including leave, benefits, employee conduct, and compliance."
        )
    )
