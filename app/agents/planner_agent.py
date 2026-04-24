from app.services.llm_service import call_gemini_json

def plan_query(question: str) -> dict:
    prompt = f"""
You are the Planner Agent in a banking support multi-agent system.

Your job:
1. Identify the user's intent.
2. Identify which domains are relevant from ONLY this list:
   - accounts
   - cards
   - fraud
   - general
3. Decide if escalation is likely needed.
4. Return ONLY valid JSON.

Rules:
- Use "accounts" for checking, savings, balances, account types.
- Use "cards" for debit cards, credit cards, fees, late fees, card declines.
- Use "fraud" for phishing, scams, suspicious links, suspicious logins, unauthorized transactions, lost/stolen cards.
- Use "general" only if no strong specific domain applies.
- Multiple domains are allowed.
- needs_escalation should be true if the query is account-specific, security-sensitive, or likely needs official support.

User question:
{question}

Return EXACTLY this JSON format:
{{
  "user_intent": "short description",
  "domains": ["accounts"],
  "needs_escalation": false,
  "reasoning": "short reason"
}}
"""
    return call_gemini_json(prompt)