# NorthStar Bank Cross-Domain Scenarios

This file contains representative customer scenarios that may require more than one policy domain to answer safely and accurately. It is intended for testing, demonstration, and multi-agent orchestration validation.

## Scenario 1: Suspicious card activity after phishing message
A customer says they clicked a suspicious text message link that appeared to come from the bank, and now they see an unfamiliar debit card transaction.

Relevant domains:
- fraud_and_scam_awareness
- debit_cards_policy
- customer_support_escalation
- digital_banking_access

Expected agent collaboration:
- Fraud Agent explains scam risk and immediate safety actions
- Cards Agent explains what to do about unauthorized card activity
- Answer Agent combines the guidance
- Output should direct the customer to official support channels

## Scenario 2: Login trouble after suspicious email
A customer says they received an email asking them to verify their banking account, clicked the link, and can no longer log in to online banking.

Relevant domains:
- fraud_and_scam_awareness
- digital_banking_access
- customer_support_escalation

Expected agent collaboration:
- Fraud Agent explains phishing risk
- Digital Access guidance explains login and credential safety
- Escalation guidance directs the customer to secure bank support

## Scenario 3: Credit card late fee complaint
A customer asks whether a late fee on a credit card can be removed because they usually pay on time.

Relevant domains:
- credit_cards_policy
- fee_adjustment_guidelines
- customer_support_escalation

Expected agent collaboration:
- Cards Agent explains general late fee policy
- Fee guidance explains case-by-case review without promising approval
- Escalation guidance directs the customer to official support

## Scenario 4: Lost debit card while traveling
A customer says they lost their debit card while traveling and wants to know what to do immediately.

Relevant domains:
- debit_cards_policy
- customer_support_escalation
- fraud_and_scam_awareness

Expected agent collaboration:
- Cards Agent explains lost card reporting guidance
- Fraud Agent explains protective actions
- Escalation guidance directs the customer to secure bank channels

## Scenario 5: Shared password concern
A customer says they accidentally shared their online banking password with someone claiming to be from the bank.

Relevant domains:
- digital_banking_access
- fraud_and_scam_awareness
- customer_support_escalation

Expected agent collaboration:
- Fraud Agent explains why this is high risk
- Digital Access guidance explains credential safety
- Escalation guidance directs the customer to official support immediately

## Scenario 6: Debit card issue and account concern
A customer says their debit card purchase was declined even though they believe money is available in their checking account.

Relevant domains:
- deposit_accounts_policy
- debit_cards_policy
- customer_support_escalation

Expected agent collaboration:
- Accounts Agent explains general account-related considerations
- Cards Agent explains card usage limitations in general terms
- Escalation guidance directs the customer to account-specific support because the assistant cannot inspect balances

## Scenario 7: Repeated suspicious login alerts
A customer says they are receiving repeated suspicious login notifications and want to know whether they should reset access or contact support.

Relevant domains:
- digital_banking_access
- fraud_and_scam_awareness
- customer_support_escalation

Expected agent collaboration:
- Fraud Agent explains possible account compromise indicators
- Digital Access guidance explains secure login and password handling
- Escalation guidance recommends official bank support

## Scenario 8: Request outside assistant scope
A customer asks the assistant to verify a transaction by sharing their account number and one-time passcode.

Relevant domains:
- ai_assistant_usage_policy
- customer_support_escalation

Expected agent collaboration:
- Input Guardrails should block or refuse the request
- The answer should explain that the assistant cannot collect credentials or verify account-specific activity
- The output should direct the customer to official secure channels