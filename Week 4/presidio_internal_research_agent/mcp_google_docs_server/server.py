# mcp_google_docs_server/server.py

from fastapi import FastAPI
from pydantic import BaseModel

from mcp_google_docs_server.google_docs_client import search_insurance_docs

app = FastAPI()


class QueryRequest(BaseModel):
    source: str
    domain: str
    query: str


@app.post("/query")
def query_google_docs(request: QueryRequest):
    if request.domain.lower() != "insurance":
        return {"results": [], "message": "Domain not supported"}

    results = search_insurance_docs(request.query)

    return {
        "source": "google_docs",
        "results": results
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3333)



# python3 -m mcp_google_docs_server.server
