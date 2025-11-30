import os
import glob
import chromadb
import google.generativeai as genai
from chromadb.utils import embedding_functions
from typing import List, Dict

class PolicyVectorStore:
    """
    Manages the ingestion and retrieval of policy documents using a Vector Database.
    """
    def __init__(self, policy_folder: str, persist_dir: str = "data/vector_store"):
        self.policy_folder = policy_folder
        self.persist_dir = persist_dir
        
        # Initialize ChromaDB (Local Vector Database)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        # Use Google's Embedding Model
        # Note: We need a wrapper to make Gemini compatible with Chroma's interface
        # For simplicity in this demo, we will use a custom embedding function logic below
        self.collection = self.client.get_or_create_collection(name="policy_docs")

    def _get_embedding(self, text: str) -> List[float]:
        """
        Wraps the Gemini Embedding API.
        """
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document",
            title="Policy Document"
        )
        return result['embedding']

    def ingest_policies(self):
        """
        Reads all files in the policy folder, chunks them, and adds them to the Vector DB.
        """
        print(f"[*] Ingesting policies from {self.policy_folder}...")
        
        # Get all files
        files = glob.glob(os.path.join(self.policy_folder, "*.*"))
        if not files:
            print("[!] No policy documents found.")
            return

        documents = []
        ids = []
        metadatas = []
        embeddings = []

        doc_id_counter = 0

        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                
                # Simple chunking (Split by paragraphs or double newlines)
                # In production, use a smarter chunker like LangChain's RecursiveCharacterTextSplitter
                chunks = text.split("\n\n")
                
                for chunk in chunks:
                    if len(chunk.strip()) < 50: # Skip tiny chunks
                        continue
                        
                    doc_id = f"doc_{doc_id_counter}"
                    documents.append(chunk)
                    ids.append(doc_id)
                    metadatas.append({"source": os.path.basename(file_path)})
                    
                    # Generate embedding
                    emb = self._get_embedding(chunk)
                    embeddings.append(emb)
                    
                    doc_id_counter += 1
                    
            except Exception as e:
                print(f"[!] Error reading {file_path}: {e}")

        # Add to ChromaDB
        if documents:
            self.collection.upsert(
                documents=documents,
                embeddings=embeddings,
                ids=ids,
                metadatas=metadatas
            )
            print(f"[*] Successfully indexed {len(documents)} policy chunks.")

    def search(self, query: str, n_results: int = 3) -> str:
        """
        Semantic search for the query against the policy database.
        Returns a formatted string of context.
        """
        # Embed the query
        query_embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query"
        )['embedding']

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        # Format results
        context_str = ""
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                source = results['metadatas'][0][i]['source']
                context_str += f"--- SOURCE: {source} ---\n{doc}\n\n"
        
        return context_str