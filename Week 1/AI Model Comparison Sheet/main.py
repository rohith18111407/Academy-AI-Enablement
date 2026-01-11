import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

from openai import OpenAI
from openai import RateLimitError
from google import genai
import boto3


# ============================================================
# Environment setup
# ============================================================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AWS_REGION = os.getenv("AWS_REGION_NAME")

# IMPORTANT: Ollama must use /api/chat
OLLAMA_API_URL = os.getenv(
    "OLLAMA_API_URL",
    "http://localhost:11434/api/chat"
)

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in .env")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in .env")
if not AWS_REGION:
    raise RuntimeError("AWS_REGION_NAME not found in .env")


# ============================================================
# Clients
# ============================================================
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Gemini client
gemini_client = genai.Client(api_key=GOOGLE_API_KEY)

# AWS Bedrock client
bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION
)


# ============================================================
# Model query implementations
# ============================================================
def query_openai(model_id, prompt):
    start = time.time()
    try:
        response = openai_client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        latency = round((time.time() - start) * 1000, 2)
        return response.choices[0].message.content, latency

    except RateLimitError:
        return (
            "ERROR: OpenAI quota exceeded. Skipping evaluation for this model.",
            None
        )
    except Exception as e:
        return f"ERROR: {str(e)}", None


def query_gemini(model_id, prompt):
    start = time.time()
    try:
        response = gemini_client.models.generate_content(
            model=model_id,
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        latency = round((time.time() - start) * 1000, 2)
        return response.text, latency

    except Exception as e:
        return f"ERROR: {str(e)}", None


def query_bedrock(model_id, prompt):
    start = time.time()

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    }

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response["body"].read())
        latency = round((time.time() - start) * 1000, 2)

        return result["content"][0]["text"], latency

    except Exception as e:
        return f"ERROR: {str(e)}", None


def query_ollama(model_id, prompt):
    """
    Correct Ollama /api/chat usage and response parsing
    """
    start = time.time()

    payload = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        r = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=120
        )
        r.raise_for_status()

        data = r.json()
        latency = round((time.time() - start) * 1000, 2)

        if "message" in data and "content" in data["message"]:
            return data["message"]["content"], latency

        return f"ERROR: Unexpected Ollama response: {data}", latency

    except Exception as e:
        return f"ERROR: Ollama call failed - {str(e)}", None


# ============================================================
# Models to evaluate
# ============================================================
MODELS_TO_EVALUATE = [
    {
        "name": "GPT-4o",
        "type": "openai",
        "model_id": "gpt-4o"
    },
    {
        "name": "Claude Sonnet (Bedrock)",
        "type": "anthropic",
        "model_id": "anthropic.claude-3-sonnet-20240229-v1:0"
    },
    {
        "name": "Gemini 1.5 Pro 001",
        "type": "google",
        "model_id": "models/gemini-1.5-pro-001"
    },
    {
        "name": "DeepSeek R1 7B",
        "type": "ollama",
        "model_id": "deepseek-r1:7b"
    }
]


# ============================================================
# Evaluation prompts
# ============================================================
EVALUATION_PROMPTS = {
    "AppDev (Code Generation)": [
        {
            "id": "appdev_fizzbuzz",
            "task_description": "Python FizzBuzz",
            "prompt": "Write a clean Python function for FizzBuzz from 1 to 100."
        }
    ],
    "Data (SQL Generation & Analysis)": [
        {
            "id": "data_sql_top_customers",
            "task_description": "Top Customers by Revenue",
            "prompt": (
                "Write an optimized SQL query to get top 5 customers "
                "by revenue in the last 6 months."
            )
        }
    ],
    "DevOps (Infrastructure Automation)": [
        {
            "id": "devops_terraform_ecs",
            "task_description": "Terraform ECS Deployment",
            "prompt": (
                "Create Terraform code to deploy a Docker application "
                "on AWS ECS with an Application Load Balancer."
            )
        }
    ]
}


# ============================================================
# Main evaluation logic
# ============================================================
def run_evaluation():
    results = []

    for model in MODELS_TO_EVALUATE:
        print(f"\nEvaluating model: {model['name']}")

        for category, prompts in EVALUATION_PROMPTS.items():
            for item in prompts:
                print(f"  - {category}: {item['task_description']}")

                if model["type"] == "openai":
                    response, latency = query_openai(
                        model["model_id"], item["prompt"]
                    )
                elif model["type"] == "anthropic":
                    response, latency = query_bedrock(
                        model["model_id"], item["prompt"]
                    )
                elif model["type"] == "google":
                    response, latency = query_gemini(
                        model["model_id"], item["prompt"]
                    )
                elif model["type"] == "ollama":
                    response, latency = query_ollama(
                        model["model_id"], item["prompt"]
                    )
                else:
                    continue

                results.append({
                    "model": model["name"],
                    "provider": model["type"],
                    "category": category,
                    "prompt_id": item["id"],
                    "task_description": item["task_description"],
                    "prompt": item["prompt"],
                    "response_text": response,
                    "latency_ms": latency,
                    "rating": "",
                    "comments": ""
                })

    return results


# ============================================================
# Entry point
# ============================================================
if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    raw_output_file = f"ai_evaluation_raw_results_{timestamp}.json"
    report_file = f"ai_evaluation_report_{timestamp}.md"

    raw_results = run_evaluation()

    with open(raw_output_file, "w", encoding="utf-8") as f:
        json.dump(raw_results, f, indent=2)

    print(f"\nRaw results saved to: {raw_output_file}")
    input("\nAdd ratings/comments in the JSON file, then press Enter to continue...")

    with open(raw_output_file, "r", encoding="utf-8") as f:
        annotated_results = json.load(f)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# AI Model Evaluation Report\n\n")

        for entry in annotated_results:
            f.write(f"## {entry['category']} - {entry['task_description']}\n")
            f.write(f"**Model:** {entry['model']}\n\n")
            f.write(f"**Latency:** {entry['latency_ms']} ms\n\n")
            f.write(f"**Rating:** {entry['rating']}\n\n")
            f.write(f"**Comments:** {entry['comments']}\n\n")
            f.write("---\n\n")

    print(f"Markdown report generated: {report_file}")
