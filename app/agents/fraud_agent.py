def run_fraud_agent(question: str, snippets: list) -> dict:
    relevant = [
        s for s in snippets
        if "fraud" in s["source"] or "digital" in s["source"] or "escalation" in s["source"]
    ]

    summary_parts = [s["content"] for s in relevant[:3]]

    return {
        "domain": "fraud",
        "summary": "\n\n".join(summary_parts) if summary_parts else "No fraud-related guidance found.",
        "evidence": relevant[:3]
    }