from google.generativeai import GenerativeModel, upload_file
import time
from compliance_agents.config import VISION_MODEL  # Import from config

class DocumentParserAgent:
    def __init__(self):
        # Use the model defined in config.py
        self.model_name = VISION_MODEL
        print(f"[*] Parser Agent initialized with model: {self.model_name}")
        
        self.system_instruction = """
        You are the 'RobustDocumentParser'.
        YOUR GOAL: Convert raw document images into structured, machine-readable text (Markdown).
        CRITICAL CAPABILITIES:
        1. Irregular Tables: Identify complex table structures. Represent strictly as Markdown.
        2. Handwriting: Transcribe messy handwriting, wrapping it in <handwritten> tags.
        OUTPUT FORMAT: Return ONLY the cleaned Markdown text.
        """
        self.model = GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_instruction
        )

    def parse_document(self, file_path: str) -> str:
        print(f"[*] Parser Agent: Uploading {file_path}...")
        try:
            uploaded_file = upload_file(file_path)
            while uploaded_file.state.name == "PROCESSING":
                time.sleep(1)
            
            response = self.model.generate_content(
                [uploaded_file, "Analyze this document and execute your system instructions to extract the data."]
            )
            return response.text
        except Exception as e:
            print(f"[!] Error parsing document: {e}")
            return f"Error: {e}"