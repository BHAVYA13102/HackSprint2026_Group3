
import sys
import os
sys.path.append(os.getcwd())

from rag.main_pipeline import HelixRAGPipeline

def run_mandatory_tests():
    print("--- 🔍 Step 9: End-to-End Stress Test ---")
    pipeline = HelixRAGPipeline()
    
    questions = [
        ("Tenure/Leave", "I am Gabrielle Davis (EMP1004). Based on the 2026 policy and my specific joining date, exactly how many total days of annual leave am I entitled to this year? Please show your calculation."),
        ("Medical/Sick", "I am Allen Robinson (EMP1002). I am feeling unwell today in my Singapore home. If I take only today off as sick leave, do I need to submit a medical certificate when I return?"),
        ("Attendance/Disciplinary", "Looking at the attendance policy, what is the specific penalty for an employee who has 6 instances of missing check-out entries in a single calendar month?"),
        ("Sabbatical/Complex", "I am Sherri Baker (EMP1015). I have been with Helix Global since early 2018 and work in the Sydney office. Am I eligible to apply for the sabbatical program right now (February 2026)?"),
        ("Regional/BankHoliday", "I am Thomas Bradley (EMP1010). Since I work in the London office, what is my total leave entitlement including bank holidays?")
    ]
    
    for category, q in questions:
        print(f"\n[TEST: {category}]")
        print(f"Q: {q}")
        result = pipeline.process_query(q)
        print("-" * 20)
        print(f"Confidence: {result['confidence']*100}%")
        print(f"Response: {result['response']}")
        if result['warnings']:
            print(f"Warnings: {result['warnings']}")
        print("=" * 50)

if __name__ == "__main__":
    run_mandatory_tests()
