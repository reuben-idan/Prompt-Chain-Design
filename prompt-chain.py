def run_prompt_chain(customer_query):
    # Stage 1: Interpret customer intent
    intent_result = f"The customer is asking for help with: {customer_query}. Primary intent: {'account access issue' if 'access' in customer_query.lower() or 'login' in customer_query.lower() else 'transaction inquiry' if 'transaction' in customer_query.lower() else 'billing issue' if 'bill' in customer_query.lower() or 'charge' in customer_query.lower() else 'general banking assistance'}."
    
    # Stage 2: Map to possible categories
    categories = []
    query_lower = customer_query.lower()
    if any(word in query_lower for word in ['access', 'login', 'password', 'locked']):
        categories.append('Account Access')
    if any(word in query_lower for word in ['transaction', 'payment', 'transfer']):
        categories.append('Transaction Inquiry')
    if any(word in query_lower for word in ['bill', 'charge', 'fee']):
        categories.append('Billing Issue')
    if any(word in query_lower for word in ['card', 'debit', 'credit']):
        categories.append('Card Services')
    if any(word in query_lower for word in ['statement', 'balance']):
        categories.append('Account Statement')
    if any(word in query_lower for word in ['loan', 'mortgage']):
        categories.append('Loan Inquiry')
    if any(word in query_lower for word in ['open', 'new account']):
        categories.append('Account Opening')
    if not categories:
        categories.append('General Information')
    category_mapping_result = f"Potential categories: {', '.join(categories[:3])}"
    
    # Stage 3: Choose most appropriate category
    selected_category = categories[0] if categories else 'General Information'
    category_selection_result = f"Selected category: {selected_category}"
    
    # Stage 4: Extract additional details
    details_needed = []
    if selected_category == 'Account Access':
        details_needed = ['account number', 'last successful login date', 'error messages']
    elif selected_category == 'Transaction Inquiry':
        details_needed = ['transaction date', 'amount', 'merchant name']
    elif selected_category == 'Billing Issue':
        details_needed = ['billing date', 'disputed amount', 'account number']
    elif selected_category == 'Card Services':
        details_needed = ['card type', 'last 4 digits', 'issue description']
    elif selected_category == 'Account Statement':
        details_needed = ['account number', 'statement period', 'delivery method']
    elif selected_category == 'Loan Inquiry':
        details_needed = ['loan type', 'loan amount', 'application status']
    elif selected_category == 'Account Opening':
        details_needed = ['account type', 'initial deposit', 'identification documents']
    else:
        details_needed = ['account number', 'specific question']
    details_extraction_result = f"Additional details needed: {', '.join(details_needed)}"
    
    # Stage 5: Generate response
    response_generation_result = f"Thank you for contacting us regarding your {selected_category.lower()} concern. To assist you better, please provide: {', '.join(details_needed)}. We're here to help resolve this quickly."
    
    return [
        intent_result,
        category_mapping_result,
        category_selection_result,
        details_extraction_result,
        response_generation_result
    ]