from app.agents.guardrails_agent import validate_input, validate_output
from app.agents.planner_agent import plan_query
from app.agents.retrieval_agent import retrieve_documents
from app.agents.accounts_agent import run_accounts_agent
from app.agents.cards_agent import run_cards_agent
from app.agents.fraud_agent import run_fraud_agent
from app.agents.answer_agent import generate_answer
from app.agents.critic_agent import critique_answer

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
    planner_result = plan_query(question)

    trace.append("retrieval")
    retrieval_result = retrieve_documents(question, planner_result["domains"])

    domain_outputs = []

    if "accounts" in planner_result["domains"]:
        trace.append("accounts_agent")
        domain_outputs.append(run_accounts_agent(question, retrieval_result["snippets"]))

    if "cards" in planner_result["domains"]:
        trace.append("cards_agent")
        domain_outputs.append(run_cards_agent(question, retrieval_result["snippets"]))

    if "fraud" in planner_result["domains"]:
        trace.append("fraud_agent")
        domain_outputs.append(run_fraud_agent(question, retrieval_result["snippets"]))

    trace.append("answer_agent")
    final_answer = generate_answer(question, planner_result, retrieval_result, domain_outputs)

    trace.append("output_guardrails")
    output_result = validate_output(final_answer)
    if not output_result["safe"]:
        final_answer = (
            "I can provide general banking guidance, but for this situation "
            "please use official bank support channels for secure assistance."
        )

    trace.append("critic_agent")
    critic_feedback = critique_answer(question, final_answer, planner_result)

    return {
        "question": question,
        "planner": planner_result,
        "matched_files": retrieval_result["matched_files"],
        "domain_outputs": domain_outputs,
        "final_answer": final_answer,
        "output_safe": output_result["safe"],
        "critic_feedback": critic_feedback,
        "trace": trace
    }