# evaluate_agents.py
import time
from typing import List, Dict
from agents.it_agent import it_agent
from agents.finance_agent import finance_agent
from agents.supervisor import supervisor_agent

# ─────────── Evaluation Runner ───────────

def run_agent(query: str) -> Dict:
    start = time.time()

    # Route query using supervisor agent
    sup_res = supervisor_agent({"input": query})
    chosen_agent = sup_res["category"]

    # Call the appropriate specialist agent
    if chosen_agent == "Finance":
        result = finance_agent({"input": query})
    else:
        result = it_agent({"input": query})

    latency = round(time.time() - start, 2)

    return {
        "query": query,
        "chosen_agent": chosen_agent,
        "output": result["output"],
        "tools_used": result["tools_used"],
        "latency": latency
    }


def evaluate_interactive() -> List[Dict]:
    print("Interactive Agent Evaluation (auto-routing via Supervisor)")
    print("Type 'exit' to finish and save the report.\n")
    results = []

    while True:
        query = input("Enter a question to evaluate: ")
        if query.lower() == "exit":
            break

        res = run_agent(query)

        # Simple heuristic metrics
        text = res["output"].lower()
        # correctness: basic check if agent name keywords appear in the answer
        correct = ("finance" in text and res["chosen_agent"] == "Finance") or \
                  ("it" in text or "vpn" in text or "software" in text and res["chosen_agent"] == "IT")
        hallucination = "i don't know" in text or "unknown" in text
        tool_success = len(res["tools_used"]) > 0

        res.update({
            "correct": correct,
            "hallucination": hallucination,
            "tool_success": tool_success
        })

        results.append(res)

        # Print results
        print("\n--- Result ---")
        print(f"Supervisor chose: {res['chosen_agent']}")
        print(f"Output: {res['output']}")
        print(f"Tools Used: {res['tools_used']}")
        print(f"Latency: {res['latency']}s")
        print(f"Correct (heuristic): {res['correct']}")
        print(f"Hallucination (heuristic): {res['hallucination']}")
        print(f"Tool Usage Success: {res['tool_success']}")
        print("\n" + "="*50 + "\n")

    return results


def save_markdown(results: List[Dict]):
    with open("evaluation_results.md", "w") as f:
        f.write("# Agent Evaluation Report\n\n")
        for r in results:
            f.write(f"## Question: {r['query']}\n")
            f.write(f"- Supervisor Chose Agent: {r['chosen_agent']}\n")
            f.write(f"- Output: {r['output']}\n")
            f.write(f"- Tools Used: {r['tools_used']}\n")
            f.write(f"- Latency (s): {r['latency']}\n")
            f.write(f"- Correct (heuristic): {r['correct']}\n")
            f.write(f"- Hallucination (heuristic): {r['hallucination']}\n")
            f.write(f"- Tool Usage Success: {r['tool_success']}\n\n")
    print("Saved evaluation_results.md")


if __name__ == "__main__":
    results = evaluate_interactive()
    if results:
        save_markdown(results)
    else:
        print("No questions were evaluated. Exiting.")
