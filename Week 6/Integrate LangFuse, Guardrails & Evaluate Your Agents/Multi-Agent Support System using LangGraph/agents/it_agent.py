from agents.llm import get_bedrock_llm
from tools.rag import load_vectorstore
from tools.web_search import get_web_search_tool
from langchain_core.messages import HumanMessage
from agents.utils import is_answerable

llm = get_bedrock_llm()
vectorstore = load_vectorstore("vectorstore/it", "data/it_docs")
web_search = get_web_search_tool()

def it_agent(state):
    query = state["input"]
    tools_used = []

    context = ""
    use_web = False  # ✅ FIX

    try:
        docs = vectorstore.similarity_search(query, k=3)
    except Exception as e:
        docs = []
        print(f"[WARNING] RAG retrieval failed: {e}")

    if docs:
        rag_context = "\n".join(d.page_content for d in docs)

        if is_answerable(llm, rag_context, query):
            context = rag_context
            tools_used.append("RAG (Internal IT Docs)")
        else:
            use_web = True
    else:
        use_web = True

    if use_web:
        tools_used.append("Web Search (Tavily)")
        results = web_search.search(query=query, max_results=3)
        context = "\n".join(results)

    prompt = f"""
You are an IT support assistant.

Context:
{context}

Question:
{query}

Answer clearly and mention which tools you used.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        "output": response.content,
        "tools_used": tools_used
    }
