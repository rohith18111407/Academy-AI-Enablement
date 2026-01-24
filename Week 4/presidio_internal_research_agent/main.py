from agents.presidio_research_agent import create_presidio_research_agent


def format_agent_output(output):
    """
    Extracts clean text from LangChain / Bedrock agent output.
    """
    if isinstance(output, list):
        # Bedrock often returns a list of message chunks
        return "\n".join(
            item.get("text", "")
            for item in output
            if item.get("type") == "text"
        )

    # Fallback (in case future versions return plain text)
    return str(output)


if __name__ == "__main__":
    agent = create_presidio_research_agent()

    print("\nPresidio Internal Research Agent")
    print("Type your question below (or type 'exit' to quit)\n")

    while True:
        query = input("Enter your query: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("\nExiting Presidio Research Agent")
            break

        response = agent.invoke({"input": query})

        formatted_output = format_agent_output(response["output"])

        print("\n" + "=" * 60)
        print("FINAL RESPONSE")
        print("=" * 60)
        print(formatted_output)
        print("=" * 60 + "\n")
