from agents.llm import get_bedrock_llm
from langchain_core.messages import HumanMessage
from langfuse import observe   # <-- updated import

llm = get_bedrock_llm()

@observe(name="Supervisor Agent")
def supervisor_agent(state):
    query = state["input"]

    prompt = f"""
Classify the following query as either IT or Finance.
Only respond with one word: IT or Finance.

Query: {query}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    category = response.content.strip()

    if category not in ["IT", "Finance"]:
        category = "IT"

    return {
        "category": category,
        "input": query
    }
