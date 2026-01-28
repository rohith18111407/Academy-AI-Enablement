# tools/web_search.py
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

def get_web_search_tool():
    """
    Tavily automatically reads TAVILY_API_KEY from env
    """
    return TavilyClient()
