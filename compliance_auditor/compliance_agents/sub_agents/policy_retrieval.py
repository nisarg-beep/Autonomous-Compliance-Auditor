from google.generativeai import GenerativeModel
from compliance_agents.tools.search_tools import PolicyVectorStore
from compliance_agents.config import RETRIEVAL_MODEL

class PolicyRetrievalAgent:
    def __init__(self, vector_store: PolicyVectorStore):
        self.vector_store = vector_store
        self.model = GenerativeModel(RETRIEVAL_MODEL)
        
    def retrieve_relevant_policies(self, document_text: str) -> str:
        print("[*] Policy Retrieval Agent: Analyzing document...")
        prompt = f"""
        Identify the top 3 specific compliance topics in this text.
        Return ONLY a comma-separated list.
        TEXT: {document_text[:4000]}
        """
        try:
            response = self.model.generate_content(prompt)
            queries = [q.strip() for q in response.text.split(',')]
            print(f"[*] Generated Queries: {queries}")
            
            aggregated_context = ""
            for query in queries:
                results = self.vector_store.search(query, n_results=2)
                aggregated_context += results + "\n"
            return aggregated_context
        except Exception as e:
            print(f"[!] Error in retrieval: {e}")
            return ""