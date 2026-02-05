
from langchain_community.llms import Ollama
import logging
from config.settings import LOCAL_LLM_MODEL
from llm.prompt_templates import PromptTemplates

class GemmaClient:
    """
    Interface for the local Gemma 3 model via Ollama.
    """
    def __init__(self):
        try:
            self.llm = Ollama(
                model=LOCAL_LLM_MODEL,
                temperature=0.1,  # Keep it deterministic for enterprise RAG
                system=PromptTemplates.SYSTEM_PERSONA
            )
            logging.info(f"Initialized GemmaClient with model: {LOCAL_LLM_MODEL}")
        except Exception as e:
            logging.critical(f"Failed to connect to local Ollama instance: {e}")
            self.llm = None

    def invoke(self, prompt):
        """
        Executes the LLM call and returns the response string.
        """
        if not self.llm:
            return "ERROR: Local LLM service (Ollama) is unavailable."
        
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logging.error(f"LLM Invocation Error: {e}")
            return f"I encountered a technical error: {str(e)}"

if __name__ == "__main__":
    client = GemmaClient()
    response = client.invoke("Test: Hello Helix Bot!")
    print(f"Gemma Response: {response}")
