
from data_ingestion.load_employee_data import load_employee_data
from data_ingestion.load_leave_data import load_leave_data
from data_ingestion.load_attendance_logs import load_attendance_logs
from preprocessing.normalization import validate_integrity

def verify_step_2():
    print("--- 🔍 Step 2 Verification ---")
    
    # Check Employee Data
    emp_df = load_employee_data()
    print(f"✅ Employee Master: {len(emp_df)} records loaded.")
    
    # Check Leave Data
    leave_df = load_leave_data()
    print(f"✅ Leave Tracker: {len(leave_df)} records loaded.")
    
    # Check Attendance Data
    att_df = load_attendance_logs()
    print(f"✅ Attendance Logs: {len(att_df)} events parsed.")
    
    # Integrity Check
    orphans = validate_integrity(emp_df, att_df)
    if not orphans:
        print("✅ Referential Integrity: All attendance logs map to valid Employee IDs.")
    else:
        print(f"⚠️ Integrity Warning: Found {len(orphans)} orphaned IDs in Attendance logs.")

if __name__ == "__main__":
    verify_step_2()
