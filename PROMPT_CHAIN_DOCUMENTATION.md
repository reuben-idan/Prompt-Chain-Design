# Intelligent Banking Support System - Prompt Chain Design

## Overview
This document describes a 5-stage prompt chain designed to process customer banking queries systematically, from initial understanding to final response generation.

## Prompt Chain Architecture

### Stage 1: Intent Interpretation
**Prompt:**
```
Analyze this customer query and identify their primary intent in 1-2 sentences:
Query: "{customer_query}"

What is the customer asking for or reporting?
```

**Explanation:**
This foundational stage focuses on understanding the core meaning behind the customer's words. By asking for the primary intent in concise language, we establish a clear baseline understanding that strips away ambiguity and focuses on the essential request. This stage is crucial because it transforms potentially confusing or verbose customer language into a clear statement of need that subsequent stages can build upon.

### Stage 2: Category Mapping
**Prompt:**
```
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
```

**Explanation:**
This stage leverages the clarified intent to identify potential classification paths. Rather than forcing an immediate decision, it allows for multiple possibilities, which is important because customer queries can sometimes span multiple service areas. The brief reasoning requirement ensures the system considers why each category might apply, creating a more thoughtful classification process that can handle edge cases and ambiguous requests.

### Stage 3: Category Selection
**Prompt:**
```
Given the customer query: "{customer_query}"
And these potential categories: {category_mapping_prompt}

Select the single most appropriate category and explain why in one sentence.
```

**Explanation:**
This decisive stage takes the multiple possibilities from Stage 2 and makes a definitive classification choice. By requiring both the original query and the potential categories as context, it ensures the final decision considers all available information. The single-sentence explanation requirement forces clarity and accountability in the decision-making process, which is essential for system transparency and debugging.

### Stage 4: Details Extraction
**Prompt:**
```
For this banking query: "{customer_query}"
Category: {category_selection_prompt}

What additional information might be needed to fully address this request?
(e.g., account number, transaction date, amount, card type, etc.)
List specific details that would help resolve the issue.
```

**Explanation:**
This stage anticipates the information gaps that typically exist in customer queries. By considering both the original query and the determined category, it can identify category-specific details that are commonly needed for resolution. This proactive approach helps prepare for efficient customer service by identifying what additional questions might need to be asked, reducing back-and-forth communication and improving resolution speed.

### Stage 5: Response Generation
**Prompt:**
```
Create a helpful, professional response to this customer:

Query: "{customer_query}"
Category: {category_selection_prompt}
Additional details needed: {details_extraction_prompt}

Provide a concise, empathetic response that addresses their concern and guides next steps.
```

**Explanation:**
The final stage synthesizes all previous analysis into a customer-facing response. By incorporating the original query, the determined category, and the identified information needs, it can craft a response that directly addresses the customer's concern while being appropriately specific to their situation. The emphasis on empathy and next steps ensures the response is both emotionally appropriate and actionable, leading to better customer satisfaction and clearer resolution paths.

## Chain Benefits

1. **Systematic Processing**: Each stage builds logically on the previous one, ensuring thorough analysis
2. **Transparency**: Each intermediate step is preserved, allowing for debugging and improvement
3. **Flexibility**: The multi-stage approach can handle complex or ambiguous queries better than single-step classification
4. **Consistency**: Standardized prompts ensure uniform processing across different customer queries
5. **Scalability**: The modular design allows for easy modification or enhancement of individual stages

## Implementation Notes

The `run_prompt_chain()` function returns all five intermediate outputs, allowing for:
- Complete audit trails of the decision-making process
- Easy debugging when responses don't meet expectations
- Potential for human oversight at any stage
- Training data collection for system improvement