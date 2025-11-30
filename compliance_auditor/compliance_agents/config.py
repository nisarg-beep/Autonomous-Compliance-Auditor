import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    load_dotenv(dotenv_path="../.env")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please ensure you have a .env file.")

# Configure globally
genai.configure(api_key=GOOGLE_API_KEY)

# 2. Model Configurations - USING GEMINI 2.5
# We use the specific preview model available in this environment
CURRENT_MODEL = "gemini-2.5-flash-preview-09-2025"

VISION_MODEL = CURRENT_MODEL
RETRIEVAL_MODEL = CURRENT_MODEL
AUDITOR_MODEL = CURRENT_MODEL

EMBEDDING_MODEL = "models/text-embedding-004"

# 3. System Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
POLICIES_DIR = os.path.join(DATA_DIR, "policies")
INPUT_DOCS_DIR = os.path.join(DATA_DIR, "input_docs")
VECTOR_STORE_DIR = os.path.join(DATA_DIR, "vector_store")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

# Ensure directories exist
os.makedirs(POLICIES_DIR, exist_ok=True)
os.makedirs(INPUT_DOCS_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)