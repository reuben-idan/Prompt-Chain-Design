# Prompt-Chain-Design
Prompt Chain Design for Intelligent Banking Support System

## Overview
This repository contains a 5-stage prompt chain implementation for processing banking customer support queries. The system systematically analyzes customer requests through intent interpretation, category mapping, selection, detail extraction, and response generation.

## Files
- `prompt-chain.py` - Main implementation with `run_prompt_chain()` function
- `PROMPT_CHAIN_DOCUMENTATION.md` - Detailed explanation of each prompt stage
- `example_usage.py` - Demonstration of the system in action

## Categories
The system classifies queries into:
- Account Opening
- Billing Issue
- Account Access
- Transaction Inquiry
- Card Services
- Account Statement
- Loan Inquiry
- General Information

## Usage
```python
from prompt_chain import run_prompt_chain

query = "I can't access my account"
results = run_prompt_chain(query)
# Returns list of 5 intermediate outputs
```

