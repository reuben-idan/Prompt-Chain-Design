# Prompt Chain Design

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)

> Intelligent Banking Support System with 5-Stage Prompt Chain Processing

## Overview

A systematic approach to processing banking customer support queries through sequential prompt chaining. The system analyzes customer requests through intent interpretation, category mapping, selection, detail extraction, and response generation.

## Features

- **Sequential Processing**: 5-stage prompt chain execution
- **Category Classification**: Supports 8 banking service categories
- **Intent Recognition**: Automated customer intent interpretation
- **Detail Extraction**: Identifies required information for resolution
- **Response Generation**: Professional customer service responses

## Banking Categories

| Category | Description |
|----------|-------------|
| Account Opening | New account creation requests |
| Billing Issue | Payment and billing disputes |
| Account Access | Login and authentication problems |
| Transaction Inquiry | Payment and transfer questions |
| Card Services | Debit/credit card related issues |
| Account Statement | Balance and statement requests |
| Loan Inquiry | Loan applications and information |
| General Information | Miscellaneous banking questions |

## Quick Start

```python
# Load the function
exec(open('prompt-chain.py').read())

# Process a customer query
query = "I can't access my account"
results = run_prompt_chain(query)

# View results
for i, result in enumerate(results, 1):
    print(f"Stage {i}: {result}")
```

## API Reference

### `run_prompt_chain(customer_query)`

**Parameters:**
- `customer_query` (str): Customer's free-text query

**Returns:**
- `list`: Five intermediate outputs from each processing stage

**Stages:**
1. Intent Interpretation
2. Category Mapping  
3. Category Selection
4. Details Extraction
5. Response Generation

## Files

```
├── prompt-chain.py     # Core implementation
├── example_usage.py    # Usage demonstration
└── README.md          # Documentation
```

## Example Output

```
Stage 1 - Intent Interpretation: The customer is asking for help with: I can't access my account. Primary intent: account access issue.

Stage 2 - Category Mapping: Potential categories: Account Access

Stage 3 - Category Selection: Selected category: Account Access

Stage 4 - Details Extraction: Additional details needed: account number, last successful login date, error messages

Stage 5 - Response Generation: Thank you for contacting us regarding your account access concern. To assist you better, please provide: account number, last successful login date, error messages. We're here to help resolve this quickly.
```

## Requirements

- Python 3.7+
- No external dependencies

## License

MIT License - see LICENSE file for details