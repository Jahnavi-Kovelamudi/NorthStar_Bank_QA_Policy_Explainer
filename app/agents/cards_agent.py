def run_cards_agent(question: str, snippets: list) -> dict:
    relevant = [
        s for s in snippets
        if "debit" in s["source"] or "credit" in s["source"] or "fee" in s["source"]
    ]

    summary_parts = [s["content"] for s in relevant[:3]]

    return {
        "domain": "cards",
        "summary": "\n\n".join(summary_parts) if summary_parts else "No card-related guidance found.",
        "evidence": relevant[:3]
    }