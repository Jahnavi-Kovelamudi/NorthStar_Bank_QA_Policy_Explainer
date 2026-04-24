import re

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

def validate_input(question: str) -> dict:
    lowered = question.lower()

    for pattern in INPUT_BLOCK_PATTERNS:
        if re.search(pattern, lowered):
            return {
                "safe": False,
                "reason": f"Blocked due to unsafe input pattern: {pattern}",
                "message": (
                    "I can help with general banking guidance, but I cannot process "
                    "passwords, PINs, one-time passcodes, or other sensitive credentials here. "
                    "Please use official bank support channels."
                )
            }

    return {
        "safe": True,
        "reason": "Input passed guardrails."
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