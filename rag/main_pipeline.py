
import re
import logging
from retrieval.query_router import QueryRouter
from retrieval.structured_query import StructuredQueryEngine
from retrieval.vector_store import VectorStoreManager
from data_ingestion.load_employee_data import load_employee_data
from data_ingestion.load_leave_data import load_leave_data
from data_ingestion.load_attendance_logs import load_attendance_logs
from rag.context_builder import ContextBuilder
from llm.llm_client import HRLLMClient
from llm.prompt_templates import PromptTemplates

from rag.response_validator import ResponseValidator

class HelixRAGPipeline:
    """
    The central orchestration engine for the Helix HR Intelligence Bot.
    """
    def __init__(self):
        # 1. Initialize Components
        print("Initializing Helix Core Components...")
        self.router = QueryRouter()
        self.v_manager = VectorStoreManager()
        self.v_db = self.v_manager.get_vector_db()
        
        # KEY BUG FIX: Auto-initialize if DB is missing
        if self.v_db is None:
            print("Vector DB missing. Building from scratch...")
            from data_ingestion.load_policy_docs import load_policy_documents
            docs = load_policy_documents()
            if docs:
                self.v_db = self.v_manager.build_index(docs)
            else:
                print("WARNING: Policy PDF not found. Vector search will be disabled.")
        
        self.llm_client = HRLLMClient()
        self.validator = ResponseValidator()
        
        # 2. Lazy Load Data
        self.emp_df = load_employee_data()
        self.leave_df = load_leave_data()
        self.att_df = load_attendance_logs()
        self.s_engine = StructuredQueryEngine(self.emp_df, self.leave_df, self.att_df)

    def process_query(self, query):
        """
        Executes the end-to-end RAG flow with validation.
        """
        # A. Intent Routing
        intent = self.router.route(query)
        emp_match = re.search(r'emp\d+', query.lower())
        emp_id = emp_match.group(0).upper() if emp_match else None
        
        structured_context = ""
        vector_context = ""

        # B. Multi-Source Retrieval
        if intent in ["structured", "hybrid"] and emp_id:
            profile = self.s_engine.get_employee_record(emp_id)
            tenure = self.s_engine.calculate_tenure(emp_id)
            attendance = self.s_engine.summarize_attendance(emp_id)
            leaves = self.s_engine.get_leave_balance(emp_id)
            structured_context = ContextBuilder.build_structured_context(profile, tenure, attendance, leaves)

        if intent in ["vector", "hybrid"]:
            if self.v_db:
                top_docs = self.v_db.similarity_search(query, k=3)
                vector_context = ContextBuilder.build_vector_context(top_docs)

        # C. Context Assembly
        full_context = f"{structured_context}\n\n{vector_context}".strip()
        
        # D. Grounded Generation
        if not full_context:
            return {
                "response": "I apologize, but I could not find any relevant HR data for this query in the Helix system.",
                "confidence": 1.0,
                "warnings": []
            }

        final_prompt = PromptTemplates.RAG_PROMPT_TEMPLATE.format(
            retrieved_context=full_context,
            user_query=query
        )
        
        raw_response = self.llm_client.invoke(final_prompt)
        
        # E. Post-Processing & Validation
        confidence_score = self.validator.calculate_confidence(raw_response, full_context, intent)
        warnings = self.validator.identify_warnings(raw_response, confidence_score)
        
        return {
            "response": raw_response,
            "confidence": confidence_score,
            "warnings": warnings,
            "intent": intent
        }


if __name__ == "__main__":
    pipeline = HelixRAGPipeline()
    test_query = "What is the policy for sick leave for EMP1002?"
    print(f"\nProcessing: {test_query}")
    print("-" * 30)
    print(pipeline.process_query(test_query))
