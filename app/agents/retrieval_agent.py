import re
from app.services.document_store import get_domain_file_map, load_documents_by_names


STOPWORDS = {
    "i", "me", "my", "we", "our", "you", "your",
    "a", "an", "the", "and", "or", "but", "if", "then",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "to", "of", "in", "on", "at", "for", "from", "with", "by",
    "this", "that", "these", "those",
    "it", "its", "as", "now", "can", "could", "should", "would",
    "do", "did", "does", "have", "has", "had"
}


DOMAIN_KEYWORDS = {
    "accounts": {"account", "accounts", "checking", "savings", "deposit", "balance"},
    "cards": {"card", "cards", "debit", "credit", "transaction", "fee", "fees", "decline", "late"},
    "fraud": {"fraud", "scam", "phishing", "suspicious", "unauthorized", "unfamiliar", "stolen", "lost", "compromised", "login", "alert", "link"},
    "general": {"policy", "support", "guide", "help", "assistant"}
}


def tokenize(text: str) -> set:
    words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    return {w for w in words if w not in STOPWORDS}


def score_text(question_tokens: set, text: str, domain_bonus_words: set) -> int:
    text_tokens = tokenize(text)
    overlap_score = len(question_tokens.intersection(text_tokens))
    bonus_score = len(text_tokens.intersection(domain_bonus_words))
    return overlap_score + bonus_score


def retrieve_documents(question: str, domains: list) -> dict:
    domain_map = get_domain_file_map()
    question_tokens = tokenize(question)

    domain_bonus_words = set()
    for domain in domains:
        domain_bonus_words.update(DOMAIN_KEYWORDS.get(domain, set()))

    candidate_files = set()
    for domain in domains:
        candidate_files.update(domain_map.get(domain, []))

    documents = load_documents_by_names(list(candidate_files))

    file_rankings = []
    for file_name, content in documents.items():
        file_score = score_text(question_tokens, file_name, domain_bonus_words)
        file_score += score_text(question_tokens, content[:2000], domain_bonus_words)

        file_rankings.append({
            "file_name": file_name,
            "score": file_score,
            "content": content
        })

    file_rankings.sort(key=lambda x: x["score"], reverse=True)

    top_files = [item for item in file_rankings if item["score"] > 0][:4]

    if not top_files:
        top_files = file_rankings[:2]

    matched_files = []
    snippets = []

    for item in top_files:
        file_name = item["file_name"]
        content = item["content"]
        matched_files.append(file_name)

        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        paragraph_rankings = []

        for para in paragraphs:
            para_score = score_text(question_tokens, para, domain_bonus_words)
            if para_score > 0:
                paragraph_rankings.append({
                    "source": file_name,
                    "content": para[:1000],
                    "score": para_score
                })

        paragraph_rankings.sort(key=lambda x: x["score"], reverse=True)

        if paragraph_rankings:
            snippets.extend(paragraph_rankings[:2])
        else:
            snippets.append({
                "source": file_name,
                "content": paragraphs[0][:1000] if paragraphs else "",
                "score": 0
            })

    snippets.sort(key=lambda x: x["score"], reverse=True)

    return {
        "matched_files": matched_files,
        "snippets": snippets[:6]
    }