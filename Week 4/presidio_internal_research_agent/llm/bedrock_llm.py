import boto3
from langchain_aws import ChatBedrock


def get_bedrock_llm():
    """
    Initializes Amazon Bedrock LLM using AWS credentials.
    Using Claude 3 Sonnet for research-grade reasoning.
    """

    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )

    return ChatBedrock(
        client=bedrock_client,
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={
            "temperature": 0,
            "max_tokens": 2048
        }
    )
