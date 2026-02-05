
import pandas as pd
from datetime import datetime
import logging

class StructuredQueryEngine:
    """
    Handles deterministic data retrieval and calculations 
    from DataFrames (CSV, Excel, JSON).
    """
    def __init__(self, emp_df, leave_df, att_df):
        self.emp_df = emp_df
        self.leave_df = leave_df
        self.att_df = att_df

    def get_employee_record(self, emp_id):
        """Fetches core profile details."""
        res = self.emp_df[self.emp_df['emp_id'] == emp_id]
        return res.iloc[0].to_dict() if not res.empty else None

    def calculate_tenure(self, emp_id):
        """Calculates precise tenure for leave eligibility."""
        emp = self.get_employee_record(emp_id)
        if not emp or pd.isna(emp.get('joining_date')):
            return None
        
        join_date = emp['joining_date']
        today = datetime.now()
        tenure_days = (today - join_date).days
        years = tenure_days // 365
        months = (tenure_days % 365) // 30
        return {"years": years, "months": months, "total_days": tenure_days}

    def summarize_attendance(self, emp_id, month=None):
        """Aggregates attendance logs for a specific period."""
        if self.att_df.empty: return None
        
        mask = (self.att_df['emp_id'] == emp_id)
        if month:
            mask &= (self.att_df['date'].dt.month == month)
            
        emp_logs = self.att_df[mask]
        return {
            "days_present": len(emp_logs),
            "records": emp_logs.to_dict('records')[:5] # Limit for context
        }

    def get_leave_balance(self, emp_id):
        """Retrieves historical leave usage records."""
        if self.leave_df.empty: return []
        res = self.leave_df[self.leave_df['emp_id'] == emp_id]
        return res.to_dict('records')
