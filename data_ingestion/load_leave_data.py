
import pandas as pd
import logging
from config.settings import LEAVE_FILE

def load_leave_data():
    """
    Loads leave tracker from Excel.
    Prepares data for cross-source correlation.
    """
    try:
        df = pd.read_excel(LEAVE_FILE)
        
        # Normalization
        df['emp_id'] = df['emp_id'].str.strip().str.upper()
        if 'start_date' in df.columns:
            df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
            
        return df
    except Exception as e:
        logging.error(f"Failure loading Leave Data: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    data = load_leave_data()
    print(f"Loaded {len(data)} leave records.")
    print(data.head(2))
