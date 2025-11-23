# prompt-chain.py
import re
from typing import List, Dict, Any

CATEGORIES = [
    "Account Opening",
    "Billing Issue", 
    "Account Access",
    "Transaction Inquiry",
    "Card Services",
    "Account Statement",
    "Loan Inquiry",
    "General Information"
]

KEYWORDS = {
    "Account Opening": ["open account", "create account", "new account", "apply for account"],
    "Billing Issue": ["charge", "billing", "bill", "overcharged", "invoice"],
    "Account Access": ["login", "log in", "password", "can't access", "locked out", "unable to sign"],
    "Transaction Inquiry": ["transaction", "withdrawal", "deposit", "payment", "pending"],
    "Card Services": ["card", "credit card", "debit", "lost card", "stolen card", "chip"],
    "Account Statement": ["statement", "monthly statement", "e-statement"],
    "Loan Inquiry": ["loan", "mortgage", "refinance", "interest rate"],
    "General Information": ["hours", "branch", "where is", "information", "how do i"]
}

AMOUNT_RE = re.compile(r"\$?\s?([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{1,2})?)")
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4}|\b\w+ \d{1,2}, \d{4}\b)")
LAST4_RE = re.compile(r"\b(\d{4})\b")

def interpret_intent(query: str) -> Dict[str, str]:
    words = query.strip().split()
    summary = " ".join(words[:20])
    lowered = query.lower()
    
    if any(k in lowered for k in ["fraud", "unauthor", "unauthorized", "stolen"]):
        label = "report-fraud"
    elif any(k in lowered for k in ["login", "password", "locked", "access"]):
        label = "account-access"
    elif any(k in lowered for k in ["open account", "apply"]):
        label = "open-account"
    elif any(k in lowered for k in ["lost card", "stolen card", "card"]):
        label = "card-issue"
    else:
        label = "general-query"
    
    return {"intent_summary": summary, "intent_label": label}

def map_to_categories(intent_summary: str, intent_label: str) -> List[Dict[str, Any]]:
    text = (intent_summary + " " + intent_label).lower()
    candidates = []
    
    for cat in CATEGORIES:
        score = 0.0
        reasons = []
        for kw in KEYWORDS.get(cat, []):
            if kw in text:
                score += 0.4
                reasons.append(f"matched '{kw}'")
        
        if cat == "Account Access" and "account-access" in intent_label:
            score += 0.3
            reasons.append("intent label suggests access issue")
        
        score = min(score, 1.0)
        if score > 0:
            candidates.append({"category": cat, "score": round(score, 2), "reason": "; ".join(reasons)})
    
    if not candidates:
        candidates.append({"category": "General Information", "score": 0.6, "reason": "no specific keywords found"})
    
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:3]

def choose_category(candidates: List[Dict[str, Any]]) -> Dict[str, str]:
    if not candidates:
        return {"chosen_category": "General Information", "explanation": "no candidates; defaulting to General Information"}
    
    top = candidates[0]
    if len(candidates) > 1 and (top["score"] - candidates[1]["score"] < 0.15):
        for c in candidates:
            if c["category"] == "Account Access":
                return {"chosen_category": c["category"], "explanation": "tie-break preferring Account Access for fast resolution"}
    
    return {"chosen_category": top["category"], "explanation": f"selected top scoring category ({top['category']})"}

def extract_additional_details(query: str, chosen_category: str) -> Dict[str, Any]:
    amount = None
    date = None
    last4 = None
    account_type = None
    transaction_ref = None
    urgent = False
    
    # Extract amounts
    m = AMOUNT_RE.search(query)
    if m:
        amount = m.group(1)
    
    # Extract dates
    d = DATE_RE.search(query)
    if d:
        date = d.group(1)
    
    # Extract last 4 digits
    for match in LAST4_RE.findall(query):
        num = int(match)
        if num < 1900:
            last4 = match
            break
    
    # Extract account type
    lowered = query.lower()
    if any(x in lowered for x in ["checking", "chequing", "current"]):
        account_type = "checking"
    elif "savings" in lowered:
        account_type = "savings"
    elif any(x in lowered for x in ["credit card", "credit"]):
        account_type = "credit"
    
    # Check urgency
    if any(x in lowered for x in ["stolen", "lost card", "fraud", "unauthorized", "unauthorised", "scam"]):
        urgent = True
    
    # Extract transaction reference
    tref = re.search(r"ref(?:erence)?[:#\s]*([A-Za-z0-9-]+)", query, re.I)
    if tref:
        transaction_ref = tref.group(1)
    
    # Generate next question
    if chosen_category in ["Transaction Inquiry", "Card Services"] and (not date or not last4):
        next_question = "Please confirm the transaction date and last 4 digits of the card/account."
    elif chosen_category == "Account Access":
        next_question = "Are you seeing an error message when logging in?"
    else:
        next_question = "Can you provide any relevant transaction IDs, dates, or card last 4 digits?"
    
    return {
        "amount": amount,
        "date": date,
        "last4": last4,
        "account_type": account_type,
        "transaction_ref": transaction_ref,
        "urgent": urgent,
        "next_question": next_question
    }

def generate_response(intent_summary: str, chosen_category: str, extracted: Dict[str, Any]) -> str:
    if extracted.get("urgent"):
        return "I'm sorry — this sounds urgent. Please call our emergency fraud line immediately at 1-800-XXX-XXXX and block your card."
    
    if chosen_category == "Account Access":
        if extracted.get("last4"):
            return f"I understand you're having trouble accessing your account. I've noted card ending {extracted['last4']}. {extracted['next_question']}"
        return f"I understand you're having trouble accessing your account. {extracted['next_question']}"
    
    if chosen_category == "Transaction Inquiry":
        if extracted.get("amount") or extracted.get("date"):
            return f"Thanks — I've found a matching transaction candidate. {extracted['next_question']}"
        return f"I can help investigate this transaction. {extracted['next_question']}"
    
    if chosen_category == "Card Services":
        return f"I can help with your card. {extracted['next_question']}"
    
    if chosen_category == "Account Opening":
        return "I can help you open a new account. Would you like checking or savings?"
    
    if chosen_category == "Billing Issue":
        return f"I'm sorry for the billing trouble. {extracted['next_question']}"
    
    if chosen_category == "Account Statement":
        return "You can download statements from the online portal. Would you like me to send instructions?"
    
    if chosen_category == "Loan Inquiry":
        return "I can connect you to our loan team. Do you want rates or application status?"
    
    return "Thanks — I can help with that. Could you provide more details?"

def run_prompt_chain(query: str) -> List[Any]:
    """
    Executes the five-step prompt chain and returns a list of five intermediate outputs:
    [intent_output, mapping_output, chosen_category_output, extracted_fields_output, response_output]
    """
    # Step 1: Interpret intent
    intent_output = interpret_intent(query)
    
    # Step 2: Map to possible categories
    mapping_output = map_to_categories(intent_output["intent_summary"], intent_output["intent_label"])
    
    # Step 3: Choose the most appropriate category
    chosen_output = choose_category(mapping_output)
    
    # Step 4: Extract additional details
    extracted_output = extract_additional_details(query, chosen_output["chosen_category"])
    
    # Step 5: Generate a short response
    response_output = generate_response(intent_output["intent_summary"], chosen_output["chosen_category"], extracted_output)
    
    return [intent_output, mapping_output, chosen_output, extracted_output, response_output]

if __name__ == "__main__":
    q = "Hi — I see a $45.00 charge on 2025-11-02 from your bank that I don't recognize. My card ending 4321. Please help, I think it's fraud."
    outs = run_prompt_chain(q)
    import json
    print(json.dumps(outs, indent=2))