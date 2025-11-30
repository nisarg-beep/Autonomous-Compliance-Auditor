import unittest
import sys
import os

# Add the project root to python path so we can import our agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compliance_agents.orchestrator import ComplianceOrchestrator

class TestComplianceAgent(unittest.TestCase):
    def setUp(self):
        """Set up the agent before each test."""
        print("\n[Test] Setting up Compliance Orchestrator...")
        # Point to the data folders we created earlier
        self.policy_folder = "data/policies"
        self.input_doc = "data/input_docs/Vendor_Service_Agreement.txt"
        self.orchestrator = ComplianceOrchestrator(policy_folder=self.policy_folder)

    def test_run_audit_flow(self):
        """
        Runs the full audit and checks if specific violations are caught.
        """
        print(f"[Test] Running audit on {self.input_doc}...")
        
        # Run the agent
        report = self.orchestrator.run_audit(self.input_doc)
        
        # --- ASSERTIONS (The Proof) ---
        # We check if the report text contains keywords related to our known violations.
        
        # 1. Check if it ran successfully
        self.assertIsNotNone(report)
        self.assertNotIn("Critical Error", report)
        
        # 2. Check for "Net 90 Days" Violation
        # The agent usually flags "90 days" or "Payment Terms"
        print("[Test] Checking for Payment Term violation...")
        self.assertTrue(
            "90 days" in report or "Payment" in report, 
            "Failed to catch the Net 90 Days violation."
        )

        # 3. Check for "Liability Cap" Violation
        print("[Test] Checking for Liability violation...")
        self.assertTrue(
            "Liability" in report or "1,000,000" in report, 
            "Failed to catch the Liability Cap violation."
        )

        # 4. Check for "California Law" Violation
        print("[Test] Checking for Governing Law violation...")
        self.assertTrue(
            "New York" in report or "California" in report or "Governing Law" in report, 
            "Failed to catch the Governing Law violation."
        )
        
        print("\n✅ TEST PASSED: All violations were detected by the AI.")

if __name__ == '__main__':
    unittest.main()