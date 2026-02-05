
import json
import pandas as pd
import logging
from config.settings import ATTENDANCE_FILE

def load_attendance_logs():
    """
    Parses semi-structured attendance logs.
    Flattens the per-employee records into a queryable format.
    """
    try:
        with open(ATTENDANCE_FILE, 'r') as f:
            raw_data = json.load(f)
            
        flat_records = []
        for emp_id, profile in raw_data.items():
            for record in profile.get('records', []):
                # Flatten the structure
                entry = {
                    'emp_id': emp_id.strip().upper(),
                    'date': pd.to_datetime(record.get('date')),
                    'check_in': record.get('check_in'),
                    'check_out': record.get('check_out'),
                    'location': record.get('location_logged')
                }
                # Preserve audit metadata
                if 'metadata' in record:
                    entry['device'] = record['metadata'].get('device')
                    entry['ip'] = record['metadata'].get('ip')
                
                flat_records.append(entry)
                
        return pd.DataFrame(flat_records)
    except Exception as e:
        logging.error(f"Failure parsing Attendance Logs: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    data = load_attendance_logs()
    print(f"Parsed {len(data)} attendance events.")
    print(data.sample(2))
