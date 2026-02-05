
import os
import sys

# Ensure root is in path for imports
sys.path.append(os.getcwd())

from llm.gemma_client import GemmaClient
from llm.prompt_templates import PromptTemplates

def test_llm_integration():
    print("--- 🔍 Step 5 Verification: LLM Connectivity ---")
    
    client = GemmaClient()
    if not client.llm:
        print("❌ FAILED: Ollama possibly not running.")
        return

    # Basic Test
    query = "Who are you?"
    prompt = PromptTemplates.RAG_PROMPT_TEMPLATE.format(
        retrieved_context="Helix HR is a leading firm.",
        user_query=query
    )
    
    print(f"Testing Prompt Injection...")
    response = client.invoke(prompt)
    print(f"✅ Success. Response: {response[:150]}...")

if __name__ == "__main__":
    test_llm_integration()
