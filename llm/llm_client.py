from langchain_community.llms import Ollama
from langchain_xai import ChatXAI
from langchain_groq import ChatGroq
import logging
import os
from dotenv import load_dotenv
from config.settings import LOCAL_LLM_MODEL, LLM_PROVIDER, XAI_MODEL, GROQ_MODEL
from llm.prompt_templates import PromptTemplates

# Load environment variables from .env if it exists
load_dotenv()

class HRLLMClient:
    """
    Unified interface for Helix HR LLM providers (Ollama, xAI, or Groq).
    """
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", LLM_PROVIDER).lower()
        self.llm = None
        
        try:
            if self.provider == "xai":
                api_key = os.getenv("XAI_API_KEY")
                self.llm = ChatXAI(
                    model=XAI_MODEL,
                    temperature=0.1,
                    api_key=api_key
                )
                logging.info(f"Initialized xAI Grok Client: {XAI_MODEL}")
                
            elif self.provider == "groq":
                api_key = os.getenv("GROQ_API_KEY")
                if not api_key:
                    logging.error("GROQ_API_KEY not found in environment.")
                self.llm = ChatGroq(
                    model=GROQ_MODEL,
                    temperature=0.1,
                    groq_api_key=api_key
                )
                logging.info(f"Initialized Groq Client: {GROQ_MODEL}")
                
            else:
                # Default to Ollama (Local)
                self.llm = Ollama(
                    model=LOCAL_LLM_MODEL,
                    temperature=0.1,
                    system=PromptTemplates.SYSTEM_PERSONA
                )
                logging.info(f"Initialized Ollama Client: {LOCAL_LLM_MODEL}")
                
        except Exception as e:
            logging.critical(f"Failed to initialize LLM provider '{self.provider}': {e}")
            self.llm = None

    def invoke(self, prompt):
        """
        Executes the LLM call and returns the response string.
        """
        if not self.llm:
            return f"ERROR: LLM provider '{self.provider}' is unavailable or misconfigured."
        
        try:
            # ChatXAI might return a Message object, while Ollama returns a string
            response = self.llm.invoke(prompt)
            if hasattr(response, 'content'):
                return response.content
            return str(response)
        except Exception as e:
            logging.error(f"LLM Invocation Error ({self.provider}): {e}")
            return f"I encountered a technical error with the {self.provider} service: {str(e)}"

if __name__ == "__main__":
    client = HRLLMClient()
    response = client.invoke("Test: Hello Helix Bot! Respond briefly.")
    print(f"Response: {response}")
