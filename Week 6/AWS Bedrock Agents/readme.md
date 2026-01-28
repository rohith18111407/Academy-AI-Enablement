# AWS BedRock Agents

## Create an Agent

1. Search for Amazon Bedrock
2. Click on Agents in left sidebar and create a new Agent named **aws_assis_agent_ro**

![alt text](image.png)

3. Select Agent resource role as **Create and use a new service role**

4. Click Select Model, select
- Categories = Anthropic
- Models = Claude 3.7 Sonnet
- Inference = EU Anthropic Claude 3.7 Sonnet

![alt text](image-1.png)

5. Click Apply

6. Instructions for the agent:

```
You will answer questions related to AWS services relying mostly on the Knowledge base provided. Make sure, in your answer to include the source where you got the information from like
"source doc _name, page #..". If you can't find the specific name or page number, just give me snippets of the original snippets of document.
For important information, include arrows like "-->" so that the users know to pay particular atention to that section.
```

![alt text](image-2.png)

![alt text](image-3.png)

7. Click on Save and then Prepare

![alt text](image-4.png)

## Test the agent

1. Type some random message

```
Hello there!
```

![alt text](image-5.png)

2. Message: 

```
How do i start an EC2 instance?
```

- The model provides the information based on its own understanding on the data it was trained and provides the result.

![alt text](image-6.png)

3. Click on Show trace

![alt text](image-7.png)

![alt text](image-8.png)

## Adding Knowledge Base to the Agent

1. Click on Add under Knowledge Base

![alt text](image-9.png)

2. Search for Knowledge bases in new tab

![alt text](image-10.png)

3. Click on Create

![alt text](image-11.png)

![alt text](image-12.png)

![alt text](image-13.png)

4. Click Next

![alt text](image-14.png)

![alt text](image-15.png)

5. Open a new tab to create S3 bucket and click on create a bucket

![alt text](image-17.png)

![alt text](image-18.png)

![alt text](image-19.png)

6. Click on Create Bucket

![alt text](image-20.png)

7. Copy the arn and paste the arn in the Knowledge base tab under S3

![alt text](image-21.png)

![alt text](image-23.png)

8. Click Next

9. Click on Select Model for Embedding

![alt text](image-25.png)

10. Click on Apply

![alt text](image-26.png)

11. Select Appropriate Vector Store and click Next

![alt text](image-27.png)

![alt text](image-28.png)

12. Before clicking on Create Knowledge Base, go to your S3 bucket and uplocad the data

![alt text](image-31.png)

![alt text](image-32.png)

![alt text](image-33.png)

13. Now click create a knowledge Base

![alt text](image-30.png)

14. Test the Knowledge base, then add it to the knowledge base in the agent builder.

## Create Action Group in Agent Builder

1. Click on Add under Action Groups

![alt text](image-34.png)

![alt text](image-35.png)

![alt text](image-36.png)

2. Click Create

![alt text](image-37.png)

3. Click on tell_time_ro and click on View of lambda function

![alt text](image-38.png)

![alt text](image-39.png)

4. Rewrite the code to display the current PST time

```
import logging
from typing import Dict, Any
from datetime import datetime
from zoneinfo import ZoneInfo
from http import HTTPStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_pacific_time() -> str:
    """Returns formatted current Pacific Time (PST/PDT)."""
    pacific_tz = ZoneInfo("America/Los_Angeles")
    now = datetime.now(pacific_tz)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler that supports:
    1. AWS Bedrock Agent invocation
    2. Direct Lambda console / API testing
    """

    logger.info("Received event: %s", event)

    try:
        current_time = get_pacific_time()

        # ✅ Case 1: Invoked by Bedrock Agent
        if "actionGroup" in event and "function" in event:
            action_group = event["actionGroup"]
            function = event["function"]
            message_version = event.get("messageVersion", 1)

            response = {
                "response": {
                    "actionGroup": action_group,
                    "function": function,
                    "functionResponse": {
                        "responseBody": {
                            "TEXT": {
                                "body": f"Current Pacific Time is: {current_time}"
                            }
                        }
                    }
                },
                "messageVersion": message_version
            }

            logger.info("Bedrock response: %s", response)
            return response

        # ✅ Case 2: Direct Lambda invocation (console / API / test)
        return {
            "statusCode": HTTPStatus.OK,
            "body": {
                "message": "Lambda executed successfully",
                "currentPacificTime": current_time
            }
        }

    except Exception as e:
        logger.exception("Unhandled exception")
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": "Internal server error"
        }

```

5. Click on Deploy

![alt text](image-40.png)

6. Click Test, create new test event and save

![alt text](image-41.png)

![alt text](image-42.png)

7. Click on Test

![alt text](image-43.png)

8. Now to map LLM agent, when the question related to time is been asked then call the new action group created as a tool, so do the following changes

- Change Action Group Type to 'Define With API schemas'

![alt text](image-44.png)

- Change Action Group Schema to Define via in-line schema editor and type to JSON

```
{
  "openapi": "3.0.0",
  "info": {
    "title": "Pacific Time Utility API",
    "version": "1.0.0",
    "description": "API to retrieve the current Pacific Time (PST/PDT). Automatically handles daylight saving time."
  },
  "paths": {
    "/current-pacific-time": {
      "post": {
        "summary": "Get current Pacific Time",
        "description": "Returns the current date and time in the America/Los_Angeles timezone (PST or PDT depending on daylight saving).",
        "operationId": "getCurrentPacificTime",
        "responses": {
          "200": {
            "description": "Successfully retrieved the current Pacific Time",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string",
                      "description": "Status message indicating successful execution.",
                      "example": "Lambda executed successfully"
                    },
                    "currentPacificTime": {
                      "type": "string",
                      "description": "The current Pacific Time in human-readable format.",
                      "example": "2026-01-27 06:10:56 PST"
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "Internal server error"
          }
        }
      }
    }
  }
}
```

![alt text](image-45.png)

9. Click Save, Save and Exit,

10. Click Save, prepare and test


bedrock-web-crawler-lambda-role-ro
bedrock-agent-execution-role-ro
web-scraper-deps-ro
