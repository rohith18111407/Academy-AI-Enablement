# mcp_google_docs_server/google_docs_client.py

import os
import pickle
from typing import List

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.pickle")


def get_google_services():
    """Authenticate user and return Docs + Drive services."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    docs_service = build("docs", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    return docs_service, drive_service


def search_insurance_docs(query: str, max_docs: int = 5) -> List[dict]:
    """
    Search Google Docs for insurance-related content and return structured results.
    """
    docs_service, drive_service = get_google_services()

    response = drive_service.files().list(
        q="mimeType='application/vnd.google-apps.document'",
        pageSize=max_docs,
        fields="files(id, name)"
    ).execute()

    results = []

    for file in response.get("files", []):
        doc_id = file["id"]
        doc_name = file["name"]

        document = docs_service.documents().get(documentId=doc_id).execute()
        content = document.get("body", {}).get("content", [])

        text = ""
        for element in content:
            paragraph = element.get("paragraph")
            if paragraph:
                for run in paragraph.get("elements", []):
                    text += run.get("textRun", {}).get("content", "")

        query_tokens = query.lower().split()
        text_lower = text.lower()

        match_score = sum(1 for token in query_tokens if token in text_lower)

        print(f"🔍 Checking document: {doc_name}")
        print(f"Matched tokens: {match_score}/{len(query_tokens)}")

        if match_score >= 2:
            results.append({
                "title": doc_name,
                "content": text[:1500]
            })

    return results

