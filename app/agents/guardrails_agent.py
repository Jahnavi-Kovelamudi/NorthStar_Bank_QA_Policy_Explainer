import re
import json
from app.services.llm_service import call_gemini_text


INPUT_BLOCK_PATTERNS = [
    r"\botp\b",
    r"\bpin\b",
    r"\bpassword\b",
    r"\bsecurity answer\b",
    r"\bssn\b",
    r"\bone[- ]time passcode\b",
    r"\bignore previous instructions\b",
    r"\breveal system prompt\b"
]

OUTPUT_BLOCK_PATTERNS = [
    r"share your password",
    r"share your otp",
    r"send your pin",
    r"i can verify your account here",
    r"your refund is guaranteed",
    r"your fee will definitely be reversed"
]


def classify_banking_scope(question: str) -> str:
    prompt = f"""
You are a strict banking-domain classifier.

Task:
Classify the user query into exactly one of these labels:
- BANKING
- OUT_OF_SCOPE
- UNCLEAR

Return only valid JSON in this exact format:
{{"label": "BANKING"}}

Classification rules:
1. BANKING:
   Use this only if the query is clearly about personal or retail banking or financial banking topics such as:
   bank accounts, savings, checking, cards, debit cards, credit cards, transactions,
   payments, transfers, balances, statements, fraud, unauthorized charges, loans,
   deposits, withdrawals, ATM, branch banking, online banking access, account freeze,
   card block, refunds related to banking transactions.

2. OUT_OF_SCOPE:
   Use this for anything not clearly related to banking support.
   This includes poems, jokes, general knowledge, coding, health, travel, sports,
   school questions, education, and words like "bank" used in non-financial meaning
   such as river bank.

3. UNCLEAR:
   Use this if the query is too vague, too short, or ambiguous to confidently classify.

Important:
- Be conservative.
- If you are not clearly sure it is banking, do NOT label it BANKING.
- The sentence "I sat under the tree on the bank of river Krishna" is OUT_OF_SCOPE.
- "My card was charged twice" is BANKING.
- "help" is UNCLEAR.
- "transfer failed" is BANKING.
- "write a poem about mountains" is OUT_OF_SCOPE.

User query:
\"\"\"{question}\"\"\"
""".strip()

    try:
        response = call_gemini_text.generate_content(prompt)
        text = response.text.strip()

        data = json.loads(text)
        label = data.get("label", "UNCLEAR").strip().upper()

        if label in {"BANKING", "OUT_OF_SCOPE", "UNCLEAR"}:
            return label

        return "UNCLEAR"

    except Exception:
        return "UNCLEAR"


def validate_input(question: str) -> dict:
    if not question or not question.strip():
        return {
            "safe": False,
            "reason": "Blocked due to empty or whitespace-only input.",
            "message": "Please enter a banking-related question so I can help you."
        }

    lowered = question.lower().strip()

    for pattern in INPUT_BLOCK_PATTERNS:
        if re.search(pattern, lowered):
            return {
                "safe": False,
                "reason": f"Blocked due to unsafe input pattern: {pattern}",
                "message": (
                    "I can help with banking-related guidance, but I cannot process "
                    "passwords, PINs, one-time passcodes, or other sensitive credentials here. "
                    "Please use official bank support channels."
                )
            }

    label = classify_banking_scope(question)

    if label == "BANKING":
        return {
            "safe": True,
            "reason": "Input passed guardrails and was classified as banking-related."
        }

    if label == "UNCLEAR":
        return {
            "safe": False,
            "reason": "Blocked because the query was too ambiguous to classify safely.",
            "message": (
                "Please ask a clear banking-related question, for example about accounts, cards, "
                "transactions, payments, loans, or fraud."
            )
        }

    return {
        "safe": False,
        "reason": "Blocked because query is outside supported banking scope.",
        "message": (
            "I am designed to help only with banking-related questions, such as accounts, cards, "
            "transactions, payments, loans, or fraud. Please ask a banking-related query."
        )
    }


def validate_output(answer: str) -> dict:
    lowered = answer.lower()

    for pattern in OUTPUT_BLOCK_PATTERNS:
        if re.search(pattern, lowered):
            return {
                "safe": False,
                "reason": f"Blocked due to unsafe output pattern: {pattern}"
            }

    return {
        "safe": True,
        "reason": "Output passed guardrails."
    }