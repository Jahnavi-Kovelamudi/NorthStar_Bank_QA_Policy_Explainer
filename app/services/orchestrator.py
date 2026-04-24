from app.agents.guardrails_agent import validate_input, validate_output
from app.agents.planner_agent import plan_query
from app.agents.retrieval_agent import retrieve_documents
from app.agents.accounts_agent import run_accounts_agent
from app.agents.cards_agent import run_cards_agent
from app.agents.fraud_agent import run_fraud_agent
from app.agents.answer_agent import generate_answer
from app.agents.critic_agent import critique_answer


def get_fallback_planner_result() -> dict:
    return {
        "user_intent": "general banking support question",
        "domains": ["general"],
        "needs_escalation": False,
        "reasoning": "Fallback planner result used due to planner failure or invalid structure."
    }


def get_fallback_critic_feedback(reason: str) -> dict:
    return {
        "approved": False,
        "completeness": "Fallback critic response used.",
        "tone": "Not evaluated due to critic failure.",
        "policy_alignment": reason,
        "suggested_fix": ""
    }


def run_workflow(question: str) -> dict:
    trace = []

    trace.append("input_guardrails")
    input_result = validate_input(question)
    if not input_result["safe"]:
        return {
            "question": question,
            "planner": {},
            "matched_files": [],
            "domain_outputs": [],
            "final_answer": input_result["message"],
            "output_safe": True,
            "critic_feedback": {
                "approved": True,
                "completeness": "Blocked safely by input guardrails.",
                "tone": "Safe",
                "policy_alignment": input_result["reason"],
                "suggested_fix": ""
            },
            "trace": trace
        }

    trace.append("planner")
    try:
        planner_result = plan_query(question)
        if not isinstance(planner_result, dict) or "domains" not in planner_result:
            planner_result = get_fallback_planner_result()
    except Exception:
        planner_result = get_fallback_planner_result()

    trace.append("retrieval")
    try:
        retrieval_result = retrieve_documents(question, planner_result.get("domains", ["general"]))
        if not isinstance(retrieval_result, dict):
            retrieval_result = {"matched_files": [], "snippets": []}
    except Exception:
        retrieval_result = {"matched_files": [], "snippets": []}

    matched_files = retrieval_result.get("matched_files", [])
    snippets = retrieval_result.get("snippets", [])

    domain_outputs = []

    if "accounts" in planner_result.get("domains", []):
        trace.append("accounts_agent")
        try:
            domain_outputs.append(run_accounts_agent(question, snippets))
        except Exception:
            domain_outputs.append({
                "domain": "accounts",
                "summary": "Accounts agent fallback: no account-specific guidance available.",
                "evidence": []
            })

    if "cards" in planner_result.get("domains", []):
        trace.append("cards_agent")
        try:
            domain_outputs.append(run_cards_agent(question, snippets))
        except Exception:
            domain_outputs.append({
                "domain": "cards",
                "summary": "Cards agent fallback: no card-specific guidance available.",
                "evidence": []
            })

    if "fraud" in planner_result.get("domains", []):
        trace.append("fraud_agent")
        try:
            domain_outputs.append(run_fraud_agent(question, snippets))
        except Exception:
            domain_outputs.append({
                "domain": "fraud",
                "summary": "Fraud agent fallback: no fraud-specific guidance available.",
                "evidence": []
            })

    if not domain_outputs:
        domain_outputs.append({
            "domain": "general",
            "summary": "No specialized domain agent was triggered. Use general banking support guidance and official support channels if the request is account-specific.",
            "evidence": []
        })

    trace.append("answer_agent")
    try:
        final_answer = generate_answer(question, planner_result, retrieval_result, domain_outputs)
        if not final_answer or not final_answer.strip():
            final_answer = (
                "I can help with general banking guidance. For account-specific or security-sensitive issues, "
                "please use official bank support channels."
            )
    except Exception:
        final_answer = (
            "I can help with general banking guidance. For account-specific or security-sensitive issues, "
            "please use official bank support channels."
        )

    trace.append("output_guardrails")
    output_result = validate_output(final_answer)
    if not output_result["safe"]:
        final_answer = (
            "I can provide general banking guidance, but for this situation "
            "please use official bank support channels for secure assistance."
        )

    trace.append("critic_agent")
    try:
        critic_feedback = critique_answer(question, final_answer, planner_result)
        if not isinstance(critic_feedback, dict):
            critic_feedback = get_fallback_critic_feedback("Fallback critic used due to invalid response structure.")
    except Exception:
        critic_feedback = get_fallback_critic_feedback("Fallback critic used due to critic failure.")

    return {
        "question": question,
        "planner": planner_result,
        "matched_files": matched_files,
        "domain_outputs": domain_outputs,
        "final_answer": final_answer,
        "output_safe": output_result["safe"],
        "critic_feedback": critic_feedback,
        "trace": trace
    }