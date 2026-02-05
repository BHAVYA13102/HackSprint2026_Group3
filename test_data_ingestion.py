from pathlib import Path

from data_ingestion.load_employee_data import load_employee_data
from data_ingestion.load_leave_data import load_leave_data
from data_ingestion.load_attendance_logs import load_attendance_logs

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "hackathon_data"

EMPLOYEE_FILE = DATA_DIR / "employee_master.csv"
LEAVE_FILE = DATA_DIR / "leave_intelligence.xlsx"
ATTENDANCE_FILE = DATA_DIR / "attendance_logs_detailed.json"


def run_ingestion_tests():
    print("🔍 Testing Employee Master ingestion...")
    employee_df = load_employee_data(EMPLOYEE_FILE)
    print("✅ Employee data loaded\n")

    print("🔍 Testing Leave Tracker ingestion...")
    leave_df = load_leave_data(LEAVE_FILE)
    print("✅ Leave data loaded\n")

    print("🔍 Testing Attendance Logs ingestion...")
    attendance_df = load_attendance_logs(ATTENDANCE_FILE)
    print("✅ Attendance data loaded\n")

    print("🎉 ALL INGESTION TESTS PASSED")


if __name__ == "__main__":
    run_ingestion_tests()
