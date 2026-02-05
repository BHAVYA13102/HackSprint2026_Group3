
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
import logging
from config.settings import PERSIST_DIRECTORY, EMBEDDING_MODEL_NAME

class VectorStoreManager:
    """
    Manages the local Vector Database for unstructured documents.
    Implements persistence and semantic indexing.
    """
    def __init__(self):
        self.persist_dir = str(PERSIST_DIRECTORY)
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        
    def build_index(self, documents):
        """
        Chunks documents and builds/persists the Chroma index.
        """
        # 1. Text Splitting (Optimized for RAG)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        
        # 2. Vector DB Initialization
        logging.info(f"Creating local Vector DB at {self.persist_dir}...")
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        
        logging.info(f"Vector DB built with {len(chunks)} semantic chunks.")
        return vector_db

    def get_vector_db(self):
        """
        Loads the existing persisted Vector DB.
        """
        if os.path.exists(self.persist_dir):
            return Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )
        return None

if __name__ == "__main__":
    from data_ingestion.load_policy_docs import load_policy_documents
    docs = load_policy_documents()
    if docs:
        manager = VectorStoreManager()
        db = manager.build_index(docs)
        print("Success: Vector Database ready.")
