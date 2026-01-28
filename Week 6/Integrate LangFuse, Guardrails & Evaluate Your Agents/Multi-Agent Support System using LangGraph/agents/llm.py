# agents/llm.py
import os
import boto3
from langchain_aws import ChatBedrock
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

def get_bedrock_llm():
    """
    Initializes Amazon Bedrock LLM using Claude 3 Sonnet.
    Credentials are loaded from .env.
    """
    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        # Session token can be added if using temporary credentials:
        # aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )

    return ChatBedrock(
        client=bedrock_client,
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={
            "temperature": 0,
            "max_tokens": 2048
        }
    )
