
import pandas as pd

def normalize_dates(df, date_columns):
    """
    Strong normalization to ISO format. 
    Crucial for referential integrity between CSV and JSON sources.
    """
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def validate_integrity(emp_df, foreign_df, key='emp_id'):
    """
    Ensures that foreign records (Leaves/Attendance) 
    map back to valid employees.
    """
    valid_ids = set(emp_df[key].unique())
    foreign_ids = set(foreign_df[key].unique())
    orphans = foreign_ids - valid_ids
    return orphans
