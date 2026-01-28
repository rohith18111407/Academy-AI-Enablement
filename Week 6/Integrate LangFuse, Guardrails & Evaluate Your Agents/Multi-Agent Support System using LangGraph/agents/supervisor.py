# agents/supervisor.py
from agents.llm import get_bedrock_llm
from langchain_core.messages import HumanMessage

llm = get_bedrock_llm()

def supervisor_agent(state):
    """
    Classifies user queries as IT or Finance.
    Returns a dict with category for routing.
    """
    query = state["input"]

    prompt = f"""
    Classify the following query as either IT or Finance.
    Only respond with one word: IT or Finance.

    Query: {query}
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    category = response.content.strip()

    if category not in ["IT", "Finance"]:
        category = "IT"  # Default fallback

    return {
        "category": category,
        "input": query
    }
