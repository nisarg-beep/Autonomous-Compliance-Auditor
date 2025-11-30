import json
from google.generativeai import GenerativeModel
from compliance_agents.config import AUDITOR_MODEL

class DiscrepancyCheckerAgent:
    def __init__(self):
        self.model = GenerativeModel(
            model_name=AUDITOR_MODEL,
            system_instruction="""
            You are a Senior Compliance Auditor. 
            OUTPUT FORMAT: JSON object with a list of "violations".
            JSON STRUCTURE:
            { "compliance_score": <int>, "violations": [{ "issue": "", "severity": "", "policy_reference": "", "document_text": "", "recommendation": "" }] }
            """
        )

    def check_compliance(self, document_text: str, policy_context: str) -> dict:
        print("[*] Discrepancy Checker: Running audit logic...")
        prompt = f"""
        Perform a compliance audit.
        --- POLICY CONTEXT ---
        {policy_context}
        --- DOCUMENT TEXT ---
        {document_text}
        """
        try:
            response = self.model.generate_content(prompt)
            json_str = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(json_str)
        except Exception as e:
            print(f"[!] Error in Auditor: {e}")
            return {"compliance_score": 0, "violations": []}