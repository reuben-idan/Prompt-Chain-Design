#!/usr/bin/env python3
"""Unit tests for prompt-chain.py"""

import unittest
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load the module directly
import importlib.util
spec = importlib.util.spec_from_file_location("prompt_chain", "prompt-chain.py")
prompt_chain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompt_chain)

run_prompt_chain = prompt_chain.run_prompt_chain
CATEGORIES = prompt_chain.CATEGORIES

class TestPromptChain(unittest.TestCase):
    
    def test_returns_five_outputs(self):
        """Test that run_prompt_chain returns exactly 5 outputs"""
        result = run_prompt_chain("I can't login")
        self.assertEqual(len(result), 5)
    
    def test_valid_category_selection(self):
        """Test that chosen category is always from valid categories"""
        test_queries = [
            "I can't access my account",
            "Strange charge on my bill", 
            "Want to open new account",
            "Lost my credit card",
            "Need account statement"
        ]
        
        for query in test_queries:
            result = run_prompt_chain(query)
            chosen_category = result[2]["chosen_category"]
            self.assertIn(chosen_category, CATEGORIES)
    
    def test_fraud_detection(self):
        """Test urgent fraud cases trigger emergency response"""
        fraud_query = "My card was stolen and I see unauthorized charges"
        result = run_prompt_chain(fraud_query)
        
        # Check urgency flag
        extracted = result[3]
        self.assertTrue(extracted["urgent"])
        
        # Check emergency response
        response = result[4]
        self.assertIn("emergency", response.lower())
        self.assertIn("1-800", response)
    
    def test_data_extraction(self):
        """Test extraction of amounts, dates, and card numbers"""
        query = "I see a $123.45 charge on 2024-01-15 on card ending 1234"
        result = run_prompt_chain(query)
        
        extracted = result[3]
        self.assertEqual(extracted["amount"], "123.45")
        self.assertEqual(extracted["date"], "2024-01-15")
        self.assertEqual(extracted["last4"], "1234")
    
    def test_account_access_category(self):
        """Test account access queries are properly categorized"""
        access_queries = [
            "can't login to my account",
            "forgot my password", 
            "account is locked out"
        ]
        
        for query in access_queries:
            result = run_prompt_chain(query)
            chosen_category = result[2]["chosen_category"]
            self.assertEqual(chosen_category, "Account Access")
    
    def test_intent_extraction(self):
        """Test intent summary and label generation"""
        query = "I want to open a new checking account"
        result = run_prompt_chain(query)
        
        intent = result[0]
        self.assertIn("intent_summary", intent)
        self.assertIn("intent_label", intent)
        self.assertTrue(len(intent["intent_summary"]) > 0)
        self.assertTrue(len(intent["intent_label"]) > 0)
    
    def test_confidence_scoring(self):
        """Test category mapping includes confidence scores"""
        query = "I have a billing question"
        result = run_prompt_chain(query)
        
        mapping = result[1]
        self.assertIsInstance(mapping, list)
        self.assertTrue(len(mapping) > 0)
        
        for candidate in mapping:
            self.assertIn("category", candidate)
            self.assertIn("score", candidate)
            self.assertIn("reason", candidate)
            self.assertGreaterEqual(candidate["score"], 0)
            self.assertLessEqual(candidate["score"], 1)
    
    def test_empty_query(self):
        """Test handling of empty or minimal queries"""
        result = run_prompt_chain("")
        self.assertEqual(len(result), 5)
        
        # Should default to General Information
        chosen_category = result[2]["chosen_category"]
        self.assertEqual(chosen_category, "General Information")

if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)