
import sys
import os

# Ensure root is in path
sys.path.append(os.getcwd())

from rag.main_pipeline import HelixRAGPipeline

def verify_rag_pipeline():
    print("--- 🔍 Step 6 Verification: Grounded RAG Pipeline ---")
    
    pipeline = HelixRAGPipeline()
    
    # Complex Cross-Source Query
    complex_query = "Am I, EMP1004, eligible for annual leave based on my joining date and the policy?"
    
    print(f"\nQUERY: {complex_query}")
    print("Executing Hybrid RAG...")
    
    response = pipeline.process_query(complex_query)
    
    print("\n" + "="*50)
    print("FINAL RESPONSE:")
    print(response)
    print("="*50)

if __name__ == "__main__":
    verify_rag_pipeline()
