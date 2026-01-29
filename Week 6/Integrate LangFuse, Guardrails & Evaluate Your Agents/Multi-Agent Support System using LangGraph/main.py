from agents.supervisor import supervisor_agent
from agents.it_agent import it_agent
from agents.finance_agent import finance_agent
from langfuse import observe   # <-- correct import

print("Multi-Agent Support System started.")
print("Type 'exit' to quit.\n")

@observe(name="User Query Session")
def handle_query(query: str):
    state = {"input": query}
    route = supervisor_agent(state)
    if route.get("output"):
        print(route["output"])
        return

    if route["category"] == "Finance":
        return finance_agent(route)
    else:
        return it_agent(route)

while True:
    query = input("Ask a question: ")
    if query.lower() == "exit":
        break

    try:
        result = handle_query(query)
        if result:
            print("\n--- Answer ---")
            print(result["output"])
            print("\nTools Used:", result["tools_used"])
            print("\n" + "=" * 50 + "\n")

    except Exception as e:
        print(f"[ERROR] Something went wrong: {e}")