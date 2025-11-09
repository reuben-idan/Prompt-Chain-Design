exec(open('prompt-chain.py').read())

if __name__ == "__main__":
    customer_query = "I can't log into my online banking account and I need to check my recent transactions"
    results = run_prompt_chain(customer_query)
    
    stage_names = ["Intent Interpretation", "Category Mapping", "Category Selection", "Details Extraction", "Response Generation"]
    
    for i, (stage_name, result) in enumerate(zip(stage_names, results), 1):
        print(f"Stage {i} - {stage_name}: {result}\n")