# agents/llm.py
import os
import boto3
from dotenv import load_dotenv
from langchain_aws import ChatBedrock

load_dotenv()

def get_bedrock_llm():
    """
    Returns a Bedrock Claude model.
    Langfuse tracing works automatically via decorators.
    """

    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    return ChatBedrock(
        client=bedrock_client,
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={
            "temperature": 0,
            "max_tokens": 2048,
        },
    )
