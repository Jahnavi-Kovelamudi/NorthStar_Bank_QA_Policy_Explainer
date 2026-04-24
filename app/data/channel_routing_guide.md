# NorthStar Bank Channel Routing Guide

This guide defines how the NorthStar Bank AI Assistant should route customers to the appropriate support channel based on request type, sensitivity, and operational risk.

## Supported Routing Principles

The assistant should route users based on the nature of the request rather than attempting to resolve all issues directly. Routing decisions should favor security, customer clarity, and operational control.

## Channel Types

### Self-service guidance in assistant
Appropriate for:
- general product education
- policy explanation
- fraud-awareness education
- digital banking safety guidance
- general fee review explanation
- clarification of non-account-specific terminology

### Official digital banking or mobile app
Appropriate for:
- reviewing account activity through official authenticated channels
- checking transaction history
- viewing product-specific disclosures available after login
- using official self-service features already available to the customer

The assistant must not pretend to complete these actions inside the chat if the chat is not authenticated for that purpose.

### Secure customer support or phone support
Appropriate for:
- lost or stolen cards
- suspected unauthorized transactions
- password reset or account lockout requiring identity verification
- disputes, complaints, or account-specific fee review
- suspicious account activity requiring investigation
- profile changes or other authenticated account support

### Human representative escalation
Appropriate for:
- repeated misunderstanding or low-confidence routing
- customer frustration or explicit request for a human
- fraud or distress scenarios
- regulated or judgment-heavy situations
- situations where multiple policy areas are involved and account-specific action is required

## Routing Rules

### Rule 1: Prefer direct answer only for general policy questions
If the user is asking for educational or policy-level information, the assistant may respond directly.

### Rule 2: Escalate when account-specific review is required
If the request depends on customer records, recent transactions, account status, or identity verification, the assistant must route to secure support.

### Rule 3: Escalate when fraud or security compromise is active
If the user indicates suspected fraud, credential compromise, suspicious transaction activity, or account takeover concern, the assistant should provide high-level immediate guidance and direct the user to official support without delay.

### Rule 4: Refuse unsafe collection of sensitive data
If the user attempts to share passwords, PINs, one-time passcodes, or similar secrets, the assistant must refuse to process that information and redirect the user to official channels.

### Rule 5: Preserve context in the final answer
When routing the user, the answer should briefly explain why routing is needed and what kind of support path is appropriate.

## Assistant Guidance

This guide should be used by the Planner Agent, output guardrails, and Critic Agent to ensure that routing decisions are consistent, safe, and easy for the user to understand.