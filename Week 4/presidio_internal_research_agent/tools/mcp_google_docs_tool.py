import requests
from typing import Optional

from langchain.tools import Tool
from langchain.callbacks.manager import CallbackManagerForToolRun


MCP_GOOGLE_DOCS_ENDPOINT = "http://localhost:3333/query"  
# 👆 This should match the MCP server URL you run for Google Docs


def query_google_docs_via_mcp(
    query: str,
    run_manager: Optional[CallbackManagerForToolRun] = None
) -> str:
    """
    Queries Google Docs via MCP server for insurance-related information.
    """

    payload = {
        "source": "google_docs",
        "domain": "insurance",
        "query": query
    }

    try:
        response = requests.post(
            MCP_GOOGLE_DOCS_ENDPOINT,
            json=payload,
            timeout=15
        )
        response.raise_for_status()

        data = response.json()

        if not data or "results" not in data:
            return "No relevant insurance information found in Google Docs."

        documents = data["results"]

        if len(documents) == 0:
            return "No matching insurance documents were found."

        # Combine all relevant document snippets
        combined_text = "\n\n".join(
            f"Document: {doc.get('title', 'Untitled')}\n{doc.get('content', '')}"
            for doc in documents
        )

        return combined_text

    except requests.exceptions.RequestException as e:
        return f"Error communicating with Google Docs MCP server: {str(e)}"


def get_mcp_google_docs_tool() -> Tool:
    """
    Returns a LangChain tool for querying Google Docs via MCP.
    """

    return Tool(
        name="mcp_google_docs_search",
        description=(
            "Use this tool to answer insurance-related questions "
            "by searching Presidio internal Google Docs via MCP. "
            "Only use it for insurance policies, coverage details, "
            "claims processes, exclusions, and compliance documents."
        ),
        func=query_google_docs_via_mcp
    )
