
from langchain_community.document_loaders import PyPDFLoader
import logging
from config.settings import POLICY_FILE

def load_policy_documents():
    """
    Loads HR policy PDF using LangChain.
    Returns a list of Document objects with content and metadata.
    """
    try:
        loader = PyPDFLoader(str(POLICY_FILE))
        documents = loader.load()
        logging.info(f"Successfully loaded {len(documents)} pages from {POLICY_FILE.name}")
        return documents
    except Exception as e:
        logging.error(f"Error loading policy PDF: {e}")
        return []

if __name__ == "__main__":
    docs = load_policy_documents()
    if docs:
        print(f"Loaded {len(docs)} pages.")
        print(f"Snippet from page 1: {docs[0].page_content[:200]}...")
