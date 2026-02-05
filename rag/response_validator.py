
import re

class ResponseValidator:
    """
    Analyzes the RAG output for potential hallucinations 
    and assigns a confidence score.
    """
    
    @staticmethod
    def calculate_confidence(response, context, intent):
        """
        Heuristic-based confidence scoring.
        Returns a score from 0.0 to 1.0.
        """
        score = 1.0
        
        # 1. Fact Check (Are key terms from context in response?)
        # Extract employee IDs or numbers from context
        context_numbers = set(re.findall(r'\d+', context))
        response_numbers = set(re.findall(r'\d+', response))
        
        # If numbers in response aren't in context -> Potential hallucination
        hallucinated_nums = response_numbers - context_numbers
        if hallucinated_nums:
            score -= 0.3 * len(hallucinated_nums)

        # 2. Source Attribution Check
        if "Source:" not in response:
            score -= 0.2

        # 3. Data Presence Check
        if "insufficient data" in response.lower():
            score = 1.0 # High confidence in knowing we DON'T know
            
        return max(0.1, min(score, 1.0))

    @staticmethod
    def identify_warnings(response, score):
        """Generates warning flags for low-confidence areas."""
        warnings = []
        if score < 0.7:
            warnings.append("Low confidence: The response contains data not explicitly found in Helix records.")
        if "Source:" not in response:
            warnings.append("Citation missing: Please verify this manually against the Policy PDF.")
        return warnings
