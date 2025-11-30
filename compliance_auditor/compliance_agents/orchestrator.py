from .sub_agents import DocumentParserAgent, PolicyRetrievalAgent, DiscrepancyCheckerAgent
from .tools.search_tools import PolicyVectorStore
from .tools.report_tools import ReportGenerator
import os

class ComplianceOrchestrator:
    """
    The Main Manager Agent.
    Responsibilities:
    1. Coordinate the workflow between sub-agents.
    2. Manage the state (passing data from one agent to the next).
    3. compile the final output.
    """
    def __init__(self, policy_folder: str = "data/policies"):
        print("[*] Orchestrator: Initializing Agents...")
        
        # 1. Initialize Tools
        # This will auto-ingest policies if the vector DB is empty
        self.vector_store = PolicyVectorStore(policy_folder=policy_folder)
        self.vector_store.ingest_policies()
        
        # 2. Initialize Sub-Agents
        self.parser = DocumentParserAgent()
        # We pass the vector store instance to the retrieval agent
        self.retriever = PolicyRetrievalAgent(vector_store=self.vector_store)
        self.auditor = DiscrepancyCheckerAgent()
        
    def run_audit(self, file_path: str) -> str:
        """
        Executes the full audit pipeline on a single file.
        Returns the final Markdown report.
        """
        filename = os.path.basename(file_path)
        print(f"\n--- Step 1: Parsing Document ({filename}) ---")
        
        # Step 1: Vision / Extraction
        document_text = self.parser.parse_document(file_path)
        
        if not document_text or "Error" in document_text[:20]:
            return f"❌ Critical Error: Could not parse document. {document_text}"
        
        print(f"\n--- Step 2: Retrieving Policies ---")
        
        # Step 2: RAG / Policy Retrieval
        # We find rules relevant to this specific document's content
        policy_context = self.retriever.retrieve_relevant_policies(document_text)
        
        if not policy_context:
            print("[!] Warning: No relevant policies found. Audit may be empty.")
            policy_context = "No specific policies found. Audit based on general best practices."

        print(f"\n--- Step 3: Auditing Discrepancies ---")
        
        # Step 3: Logic / Auditing
        audit_result = self.auditor.check_compliance(
            document_text=document_text, 
            policy_context=policy_context
        )
        
        # Step 4: Reporting
        print(f"\n--- Step 4: Generating Report ---")
        final_report = ReportGenerator.generate_markdown_report(
            filename=filename,
            violations=audit_result.get('violations', []),
            compliance_score=audit_result.get('compliance_score', 0)
        )
        
        return final_report