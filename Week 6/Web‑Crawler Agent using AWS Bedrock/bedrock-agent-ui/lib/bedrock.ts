import { BedrockAgentRuntimeClient } from "@aws-sdk/client-bedrock-agent-runtime";

export const bedrockClient = new BedrockAgentRuntimeClient({
  region: process.env.AWS_REGION || "us-east-1",
});
