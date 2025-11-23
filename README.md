# Banking Support Prompt Chain

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 5-stage prompt chain for intelligent banking customer support query processing

## Overview

This system processes banking customer queries through a sequential 5-stage prompt chain:
1. **Intent Interpretation** - Extract customer intent and generate summary
2. **Category Mapping** - Map to banking service categories with confidence scores
3. **Category Selection** - Choose single best category with tie-breaking logic
4. **Detail Extraction** - Extract structured data (amounts, dates, account info)
5. **Response Generation** - Generate empathetic customer service response

## Categories

- Account Opening
- Billing Issue
- Account Access
- Transaction Inquiry
- Card Services
- Account Statement
- Loan Inquiry
- General Information

## Usage

### Basic Usage
```python
from prompt_chain import run_prompt_chain

query = "I can't login to my account"
results = run_prompt_chain(query)
# Returns list of 5 intermediate outputs
```

### Direct Execution
```bash
python prompt-chain.py
```

### Custom Query
```python
python -c "
from prompt_chain import run_prompt_chain
import json
results = run_prompt_chain('Your query here')
print(json.dumps(results, indent=2))
"
```

## Output Format

The `run_prompt_chain()` function returns a list of 5 elements:

1. **Intent Output** (dict): `{"intent_summary": "...", "intent_label": "..."}`
2. **Category Mapping** (list): `[{"category": "...", "score": 0.8, "reason": "..."}]`
3. **Category Selection** (dict): `{"chosen_category": "...", "explanation": "..."}`
4. **Extracted Details** (dict): `{"amount": "...", "date": "...", "last4": "...", "urgent": false, ...}`
5. **Response** (str): Customer service response text

## Features

- **Regex Extraction**: Automatically extracts amounts, dates, card numbers, transaction references
- **Urgency Detection**: Identifies fraud/security cases for immediate escalation
- **Confidence Scoring**: Categories scored 0-1 with reasoning
- **Tie-Breaking**: Prefers Account Access for faster resolution
- **JSON Structured**: All outputs in structured JSON format

## Testing

Run unit tests:
```bash
python test_prompt_chain.py
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Implementation Notes

This is a deterministic mock implementation for testing. In production, replace the heuristic functions with actual LLM API calls using the same prompt templates defined in `PROMPT_DESIGN.md`.

## Files

- `prompt-chain.py` - Main implementation
- `test_prompt_chain.py` - Unit tests
- `PROMPT_DESIGN.md` - Detailed prompt specifications
- `README.md` - This documentation