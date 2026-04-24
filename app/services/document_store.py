import os
from app.config import DATA_DIR

def load_documents_by_names(file_names):
    documents = {}
    for file_name in file_names:
        path = os.path.join(DATA_DIR, file_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                documents[file_name] = f.read()
    return documents

def get_domain_file_map():
    return {
        "accounts": [
            "deposit_accounts_policy.md",
            "service_actions_matrix.md",
            "channel_routing_guide.md",
            "ai_assistant_usage_policy.md"
        ],
        "cards": [
            "debit_cards_policy.md",
            "credit_cards_policy.md",
            "fee_adjustment_guidelines.md",
            "service_actions_matrix.md",
            "channel_routing_guide.md",
            "ai_assistant_usage_policy.md"
        ],
        "fraud": [
            "fraud_and_scam_awareness.md",
            "fraud_response_playbook.md",
            "digital_banking_access.md",
            "customer_support_escalation.md",
            "service_actions_matrix.md",
            "channel_routing_guide.md",
            "ai_assistant_usage_policy.md"
        ],
        "general": [
            "ai_assistant_usage_policy.md",
            "service_actions_matrix.md",
            "channel_routing_guide.md"
        ]
    }