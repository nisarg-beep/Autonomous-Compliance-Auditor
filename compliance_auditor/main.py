import os 
import sys 
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compliance_agents.orchestrator import ComplianceOrchestrator

def main(): """ Main entry point for the Autonomous Compliance Auditor. """ # 1. Load Environment Variables (API Keys) load_dotenv() if not os.getenv("GOOGLE_API_KEY"): print("[!] Error: GOOGLE_API_KEY not found in .env file.") return

print("--- Autonomous Compliance Auditor Starting ---")

# 2. Configuration
# In a real app, these might come from command line args
input_doc_path = "data/input_docs/Vendor_Service_Agreement.txt"
policy_folder = "data/policies/"

# Check if files exist to prevent crash
if not os.path.exists(input_doc_path):
    print(f"[!] Warning: Input document not found at {input_doc_path}")
    print("    Please place a file there to test.")
    # We continue so the code structure initializes, but it will likely fail later if not fixed.

# 3. Initialize the Orchestrator
# This spins up the sub-agents and connects to the vector store
auditor = ComplianceOrchestrator(policy_folder=policy_folder)

# 4. Run the Audit Workflow
print(f"\n[*] Starting Audit for: {input_doc_path}")
audit_report = auditor.run_audit(input_doc_path)

# 5. Output Results
print("\n" + "="*50)
print("FINAL COMPLIANCE REPORT")
print("="*50)
print(audit_report)
print("="*50)

# Optional: Save to file
with open("data/audit_report.md", "w") as f:
    f.write(audit_report)
print("\n[*] Report saved to data/audit_report.md")
if __name__ == "__main__":
    main()