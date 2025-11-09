from prompt_chain import run_prompt_chain

# Example usage
if __name__ == "__main__":
    # Test query
    customer_query = "I can't log into my online banking account and I need to check my recent transactions"
    
    # Run the prompt chain
    results = run_prompt_chain(customer_query)
    
    # Display results
    stage_names = [
        "Intent Interpretation",
        "Category Mapping", 
        "Category Selection",
        "Details Extraction",
        "Response Generation"
    ]
    
    print("=== BANKING SUPPORT PROMPT CHAIN RESULTS ===\n")
    
    for i, (stage_name, result) in enumerate(zip(stage_names, results), 1):
        print(f"STAGE {i}: {stage_name}")
        print("-" * 50)
        print(result)
        print("\n")