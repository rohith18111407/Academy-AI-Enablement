from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

def get_web_search_tool():
    """
    Web Search Tool for external research.

    Used for:
    - Industry benchmarks
    - Market trends
    - Regulatory updates
    - Compliance comparisons

    NOT used for internal Presidio documents.
    """

    return TavilySearchResults(
        max_results=3,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False
    )
