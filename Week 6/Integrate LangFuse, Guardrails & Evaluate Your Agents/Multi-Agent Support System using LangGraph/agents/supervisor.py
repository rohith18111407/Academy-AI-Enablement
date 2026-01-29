from agents.llm import get_bedrock_llm
from langchain_core.messages import HumanMessage
from langfuse import observe   # <-- updated import
from sentence_transformers import SentenceTransformer, util

llm = get_bedrock_llm()
model = SentenceTransformer('all-MiniLM-L6-v2')

def checkAbusive(query:str):
   abuse_patterns = [
    "you are stupid",
    "i hate you",
    "idiot",
    "shut up",
    "dumb",
    "kill yourself",
    "you are useless",
    "stupid question",
    "nonsense",

]
   pattern_embeddings = model.encode(abuse_patterns, convert_to_tensor=True)
   def is_abusive(question: str) -> bool:
    question_embedding = model.encode(question, convert_to_tensor=True)
    cosine_scores = util.cos_sim(question_embedding, pattern_embeddings)
    max_score = cosine_scores.max().item()
    return max_score > 0.5


   def check_abuse(question: str) -> dict:
        result = is_abusive(question)
        return result
   return check_abuse(query)

@observe(name="Supervisor Agent")
def supervisor_agent(state):
    query = state["input"]
    if query:
        result = checkAbusive(query)
        if result:
            return {"output" : "Sorry I'm unable to proceed with your request"}


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