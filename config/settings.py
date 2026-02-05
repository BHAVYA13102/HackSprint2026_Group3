
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "hackathon_data"

# Data Files
EMPLOYEE_FILE = DATA_DIR / "employee_master.csv"
ATTENDANCE_FILE = DATA_DIR / "attendance_logs_detailed.json"
LEAVE_FILE = DATA_DIR / "leave_intelligence.xlsx"
POLICY_FILE = DATA_DIR / "Helix_Pro_Policy_v2.pdf"

# Settings
PERSIST_DIRECTORY = BASE_DIR / "chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LOCAL_LLM_MODEL = "gemma3:4b"

# LLM Provider: 'ollama', 'xai', or 'groq'
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq") 
XAI_MODEL = "grok-beta"
GROQ_MODEL = "llama-3.3-70b-versatile" # Premium fast model
