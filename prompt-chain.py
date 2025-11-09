def run_prompt_chain(customer_query):
    """
    Execute a 5-stage prompt chain for banking customer support.
    
    Args:
        customer_query (str): The customer's free-text query
        
    Returns:
        list: Five intermediate outputs from each stage
    """
    
    # Stage 1: Interpret customer intent
    intent_prompt = f"""
    Analyze this customer query and identify their primary intent in 1-2 sentences:
    Query: "{customer_query}"
    
    What is the customer asking for or reporting?
    """
    
    # Stage 2: Map to possible categories
    category_mapping_prompt = f"""
    Based on this customer intent: {intent_prompt}
    
    From these banking categories, which ones could potentially apply?
    - Account Opening
    - Billing Issue  
    - Account Access
    - Transaction Inquiry
    - Card Services
    - Account Statement
    - Loan Inquiry
    - General Information
    
    List 1-3 most relevant categories with brief reasoning.
    """
    
    # Stage 3: Choose most appropriate category
    category_selection_prompt = f"""
    Given the customer query: "{customer_query}"
    And these potential categories: {category_mapping_prompt}
    
    Select the single most appropriate category and explain why in one sentence.
    """
    
    # Stage 4: Extract additional details
    details_extraction_prompt = f"""
    For this banking query: "{customer_query}"
    Category: {category_selection_prompt}
    
    What additional information might be needed to fully address this request?
    (e.g., account number, transaction date, amount, card type, etc.)
    List specific details that would help resolve the issue.
    """
    
    # Stage 5: Generate response
    response_generation_prompt = f"""
    Create a helpful, professional response to this customer:
    
    Query: "{customer_query}"
    Category: {category_selection_prompt}
    Additional details needed: {details_extraction_prompt}
    
    Provide a concise, empathetic response that addresses their concern and guides next steps.
    """
    
    # Return all intermediate outputs
    return [
        intent_prompt,
        category_mapping_prompt,
        category_selection_prompt,
        details_extraction_prompt,
        response_generation_prompt
    ]