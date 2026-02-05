
import sys
import os
sys.path.append(os.getcwd())

from rag.main_pipeline import HelixRAGPipeline

def test_guardrails():
    print("--- 🔍 Step 7 Verification: Trust & Confidence ---")
    pipeline = HelixRAGPipeline()
    
    query = "What is the probation period length in the London office?"
    print(f"\nQuery: {query}")
    
    result = pipeline.process_query(query)
    
    print(f"\nResponse Confidence: {result['confidence'] * 100}%")
    if result['warnings']:
        print(f"⚠️ Warnings Detected: {result['warnings']}")
    
    print("\nPROCESSED RESPONSE:")
    print(result['response'])

if __name__ == "__main__":
    test_guardrails()
