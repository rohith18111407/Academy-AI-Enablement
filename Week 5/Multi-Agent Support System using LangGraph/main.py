from agents.supervisor import supervisor_agent
from agents.it_agent import it_agent
from agents.finance_agent import finance_agent

print("Multi-Agent Support System started.")
print("Type 'exit' to quit.\n")

while True:
    query = input("Ask a question: ")
    if query.lower() == "exit":
        break

    try:
        state = {"input": query}

        route = supervisor_agent(state)

        if route["category"] == "Finance":
            result = finance_agent(route)
        else:
            result = it_agent(route)

        print("\n--- Answer ---")
        print(result["output"])
        print("\nTools Used:", result["tools_used"])
        print("\n" + "="*50 + "\n")

    except Exception as e:
        print(f"[ERROR] Something went wrong: {e}")
