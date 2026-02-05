
import pandas as pd
import logging
from config.settings import EMPLOYEE_FILE

def load_employee_data():
    """
    Loads and cleans the employee master records.
    Ensures date normalization for tenure calculations.
    """
    try:
        df = pd.read_csv(EMPLOYEE_FILE)
        
        # Data Normalization
        df['joining_date'] = pd.to_datetime(df['joining_date'], errors='coerce')
        df['emp_id'] = df['emp_id'].str.strip().str.upper()
        
        # Data Quality Check
        if df['emp_id'].isnull().any():
            logging.warning("Missing Employee IDs detected and dropped.")
            df = df.dropna(subset=['emp_id'])
            
        return df
    except Exception as e:
        logging.error(f"Critical failure loading Employee Data: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    data = load_employee_data()
    print(f"Loaded {len(data)} employee records.")
    print(data.head(2))
