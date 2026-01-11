import requests
from config import OLLAMA_BASE_URL, LLM_MODEL

def generate_answer(prompt: str):
    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={"model": LLM_MODEL, "prompt": prompt, "stream": False}
    )
    resp.raise_for_status()
    return resp.json().get("response", "").strip()
