def run_prompt_chain(customer_query):
    """Execute 5-stage banking support prompt chain with improved prompts."""
    
    # Stage 1: Intent Interpretation
    intent_prompt = f"""You are a banking customer service analyst. Analyze this customer query and extract the core intent.

Customer Query: "{customer_query}"

Instructions:
- Identify what the customer specifically wants or needs
- Determine the urgency level (low/medium/high)
- Note any emotional indicators (frustrated, confused, urgent)
- Provide a clear 1-sentence summary of their primary intent

Format your response as:
Intent: [clear description]
Urgency: [low/medium/high]
Emotion: [neutral/frustrated/confused/urgent]"""

    # Simulate LLM response for Stage 1
    urgency = "high" if any(word in customer_query.lower() for word in ["urgent", "immediately", "asap", "emergency"]) else "medium" if any(word in customer_query.lower() for word in ["can't", "unable", "won't", "problem"]) else "low"
    emotion = "frustrated" if any(word in customer_query.lower() for word in ["can't", "won't", "problem", "issue"]) else "confused" if "how" in customer_query.lower() or "what" in customer_query.lower() else "neutral"
    
    intent_result = f"Intent: Customer needs assistance with {customer_query.lower()}\nUrgency: {urgency}\nEmotion: {emotion}"

    # Stage 2: Category Mapping
    category_mapping_prompt = f"""You are a banking service categorization expert. Map this customer intent to relevant banking service categories.

Customer Intent: {intent_result}
Original Query: "{customer_query}"

Available Categories:
- Account Opening: New account creation, account types, requirements
- Billing Issue: Disputes, unexpected charges, payment problems
- Account Access: Login issues, password resets, account lockouts
- Transaction Inquiry: Payment status, transfer questions, transaction history
- Card Services: Card issues, replacements, activations, limits
- Account Statement: Balance inquiries, statement requests, account summaries
- Loan Inquiry: Loan applications, rates, payment schedules, refinancing
- General Information: Hours, locations, services, general questions

Instructions:
- List 1-3 most relevant categories with confidence scores (1-10)
- Explain why each category applies
- Consider overlapping categories

Format: Category Name (confidence): reasoning"""

    # Simulate LLM response for Stage 2
    categories = []
    query_lower = customer_query.lower()
    
    if any(word in query_lower for word in ['access', 'login', 'password', 'locked', 'sign in']):
        categories.append('Account Access (9): Query mentions login/access issues')
    if any(word in query_lower for word in ['transaction', 'payment', 'transfer', 'money']):
        categories.append('Transaction Inquiry (8): Query involves money movement or payments')
    if any(word in query_lower for word in ['bill', 'charge', 'fee', 'dispute']):
        categories.append('Billing Issue (8): Query mentions charges or billing concerns')
    if any(word in query_lower for word in ['card', 'debit', 'credit', 'atm']):
        categories.append('Card Services (9): Query specifically about card-related issues')
    if any(word in query_lower for word in ['statement', 'balance', 'account summary']):
        categories.append('Account Statement (8): Query requests account information')
    if any(word in query_lower for word in ['loan', 'mortgage', 'credit line']):
        categories.append('Loan Inquiry (9): Query about lending products')
    if any(word in query_lower for word in ['open', 'new account', 'create']):
        categories.append('Account Opening (9): Query about new account creation')
    
    if not categories:
        categories.append('General Information (6): Query requires general banking assistance')
    
    category_mapping_result = '\n'.join(categories[:3])

    # Stage 3: Category Selection
    category_selection_prompt = f"""You are a banking service router. Select the single best category for this customer query.

Customer Query: "{customer_query}"
Intent Analysis: {intent_result}
Potential Categories: {category_mapping_result}

Decision Criteria:
- Primary issue takes precedence over secondary concerns
- Choose the category that requires immediate attention
- Consider which department can best resolve the issue

Provide:
Selected Category: [category name]
Confidence Level: [1-10]
Reasoning: [one clear sentence explaining the choice]
Alternative: [backup category if primary fails]"""

    # Simulate LLM response for Stage 3
    selected_category = categories[0].split(' (')[0] if categories else 'General Information'
    confidence = categories[0].split('(')[1].split(')')[0] if categories and '(' in categories[0] else '7'
    
    category_selection_result = f"""Selected Category: {selected_category}
Confidence Level: {confidence}
Reasoning: This category best matches the primary concern expressed in the customer query.
Alternative: General Information"""

    # Stage 4: Details Extraction
    details_extraction_prompt = f"""You are a banking support specialist preparing for customer assistance. Identify required information to resolve this query.

Customer Query: "{customer_query}"
Selected Category: {category_selection_result}
Customer Intent: {intent_result}

For {selected_category} issues, determine:
- Essential information needed immediately
- Optional information that would help
- Security verification requirements
- Potential follow-up questions

Categorize as:
REQUIRED: [critical information needed]
HELPFUL: [additional useful details]
SECURITY: [verification needed]
FOLLOW-UP: [potential next questions]"""

    # Simulate LLM response for Stage 4
    details_map = {
        'Account Access': {
            'REQUIRED': 'Account number, registered phone number',
            'HELPFUL': 'Last successful login date, error messages received',
            'SECURITY': 'Identity verification, security questions',
            'FOLLOW-UP': 'Password reset preferences, two-factor authentication setup'
        },
        'Transaction Inquiry': {
            'REQUIRED': 'Transaction date, approximate amount',
            'HELPFUL': 'Merchant name, transaction type',
            'SECURITY': 'Account verification, last 4 digits of card',
            'FOLLOW-UP': 'Dispute process, transaction limits'
        },
        'Billing Issue': {
            'REQUIRED': 'Billing date, disputed amount',
            'HELPFUL': 'Account number, description of issue',
            'SECURITY': 'Account holder verification',
            'FOLLOW-UP': 'Refund timeline, prevention measures'
        },
        'Card Services': {
            'REQUIRED': 'Card type, last 4 digits',
            'HELPFUL': 'Issue description, when problem started',
            'SECURITY': 'Cardholder verification, security code',
            'FOLLOW-UP': 'Replacement timeline, temporary solutions'
        }
    }
    
    details = details_map.get(selected_category, {
        'REQUIRED': 'Account number, nature of inquiry',
        'HELPFUL': 'Specific questions, preferred contact method',
        'SECURITY': 'Identity verification',
        'FOLLOW-UP': 'Additional services needed'
    })
    
    details_extraction_result = f"""REQUIRED: {details['REQUIRED']}
HELPFUL: {details['HELPFUL']}
SECURITY: {details['SECURITY']}
FOLLOW-UP: {details['FOLLOW-UP']}"""

    # Stage 5: Response Generation
    response_generation_prompt = f"""You are a professional banking customer service representative. Craft a helpful response to this customer.

Customer Query: "{customer_query}"
Category: {category_selection_result}
Customer Intent: {intent_result}
Required Information: {details_extraction_result}

Response Guidelines:
- Acknowledge their specific concern
- Show empathy for their situation
- Clearly state what information you need
- Explain why the information is necessary
- Provide next steps or timeline
- Maintain professional, helpful tone
- Keep response concise (2-3 sentences)

Generate a complete customer service response."""

    # Simulate LLM response for Stage 5
    emotion_acknowledgment = {
        'frustrated': "I understand this situation is frustrating, and I'm here to help resolve it quickly.",
        'confused': "I can see you have questions, and I'll be happy to clarify everything for you.",
        'urgent': "I recognize this is urgent for you, and we'll work to address this immediately.",
        'neutral': "Thank you for contacting us, and I'm ready to assist you today."
    }
    
    acknowledgment = emotion_acknowledgment.get(emotion, emotion_acknowledgment['neutral'])
    required_info = details['REQUIRED']
    
    response_generation_result = f"""{acknowledgment} To resolve your {selected_category.lower()} concern effectively, I'll need to collect some information: {required_info}. This helps us verify your identity and provide the most accurate assistance for your specific situation."""

    return [
        intent_result,
        category_mapping_result,
        category_selection_result,
        details_extraction_result,
        response_generation_result
    ]