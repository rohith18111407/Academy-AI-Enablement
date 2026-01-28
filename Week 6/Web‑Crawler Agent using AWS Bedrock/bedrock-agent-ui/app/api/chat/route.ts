import { NextResponse } from "next/server";
import { InvokeAgentCommand } from "@aws-sdk/client-bedrock-agent-runtime";
import { bedrockClient } from "@/lib/bedrock";
import { v4 as uuidv4 } from "uuid";

export async function POST(req: Request) {
  try {
    const { message } = await req.json();

    const command = new InvokeAgentCommand({
      agentId: process.env.BEDROCK_AGENT_ID!,
      agentAliasId: process.env.BEDROCK_AGENT_ALIAS_ID!,
      sessionId: uuidv4(),
      inputText: message,
    });

    const response = await bedrockClient.send(command);

    let finalText = "";

    if (response.completion) {
      for await (const chunk of response.completion) {
        if (chunk.chunk?.bytes) {
          finalText += new TextDecoder().decode(chunk.chunk.bytes);
        }
      }
    }

    return NextResponse.json({ answer: finalText });
  } catch (err: any) {
    console.error(err);
    return NextResponse.json(
      { error: "Failed to invoke Bedrock agent" },
      { status: 500 }
    );
  }
}
