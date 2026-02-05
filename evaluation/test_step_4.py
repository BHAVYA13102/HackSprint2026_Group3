
from data_ingestion.load_employee_data import load_employee_data
from data_ingestion.load_leave_data import load_leave_data
from data_ingestion.load_attendance_logs import load_attendance_logs
from retrieval.structured_query import StructuredQueryEngine
from retrieval.query_router import QueryRouter
from retrieval.vector_store import VectorStoreManager

def test_hybrid_retrieval():
    print("--- 🔍 Step 4 Verification: Hybrid Retrieval ---")
    
    # 1. Load Data
    emp_df = load_employee_data()
    leave_df = load_leave_data()
    att_df = load_attendance_logs()
    
    # 2. Init Engines
    s_engine = StructuredQueryEngine(emp_df, leave_df, att_df)
    v_manager = VectorStoreManager()
    v_db = v_manager.get_vector_db()
    router = QueryRouter()
    
    # 3. Scenario Test: Hybrid Query
    query = "I am Gabrielle Davis (EMP1004). How many total days of leave am I entitled to?"
    intent = router.route(query)
    print(f"Query: {query}\nRouted Intent: {intent}")
    
    if intent in ["structured", "hybrid"]:
        profile = s_engine.get_employee_record("EMP1004")
        tenure = s_engine.calculate_tenure("EMP1004")
        print(f"  [Structured] Found Profile: {profile['name']}, Tenure: {tenure['years']} years")
        
    if intent in ["vector", "hybrid"]:
        results = v_db.similarity_search(query, k=2)
        print(f"  [Vector] Found {len(results)} relevant policy snippets.")

if __name__ == "__main__":
    test_hybrid_retrieval()
