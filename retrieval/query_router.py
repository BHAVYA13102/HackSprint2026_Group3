
import re

class QueryRouter:
    """
    Intelligently routes queries to the appropriate retriever.
    """
    def __init__(self):
        # Keywords for intent classification
        self.fact_keywords = ["who is", "id", "joining", "salary", "role", "email"]
        self.policy_keywords = ["policy", "rule", "guideline", "dress code", "working hours", "probation"]
        self.temporal_keywords = ["attendance", "present", "clock", "leave", "holiday", "sabbatical"]

    def route(self, query):
        """
        Determines the retrieval path: 'structured', 'vector', or 'hybrid'.
        """
        query_low = query.lower()
        emp_match = re.search(r'emp\d+', query_low)
        
        has_policy = any(k in query_low for k in self.policy_keywords)
        has_temporal = any(k in query_low for k in self.temporal_keywords)
        has_fact = any(k in query_low for k in self.fact_keywords)
        
        # Logic 1: If it asks for policy + has a specific employee ID -> Hybrid
        if has_policy and emp_match:
            return "hybrid"
        
        # Logic 2: If it's about policy only -> Vector
        if has_policy:
            return "vector"
            
        # Logic 3: If it's about facts or attendance -> Structured
        if has_fact or has_temporal or emp_match:
            return "structured"
            
        # Default fallback
        return "hybrid"

if __name__ == "__main__":
    router = QueryRouter()
    print(f"Query: 'What is the dress code?' -> {router.route('What is the dress code?')}")
    print(f"Query: 'How many days was EMP1001 present?' -> {router.route('How many days was EMP1001 present?')}")
    print(f"Query: 'Is EMP1004 eligible for sabbatical?' -> {router.route('Is EMP1004 eligible for sabbatical?')}")
