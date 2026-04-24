def run_accounts_agent(question: str, snippets: list) -> dict:
    relevant = [
        s for s in snippets
        if "deposit" in s["source"] or "account" in s["source"]
    ]

    summary_parts = [s["content"] for s in relevant[:3]]

    return {
        "domain": "accounts",
        "summary": "\n\n".join(summary_parts) if summary_parts else "No account-related guidance found.",
        "evidence": relevant[:3]
    }