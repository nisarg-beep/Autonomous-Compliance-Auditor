Autonomous Compliance Auditor 🛡️

A Multi-Agent System for Automated Document Compliance Verification

Capstone Project: Kaggle AI Agents Intensive 2025

Track: Enterprise Agents

📖 Overview

Organizations lack a reliable, efficient way to verify if complex incoming documents adhere to internal policies. Manual review is slow, inconsistent, and prone to human error—especially when dealing with irregular tabular data or handwritten forms.

The Autonomous Compliance Auditor employs a consortium of specialized AI agents to:

Extract data from complex documents (PDFs, Images) using Vision-Language Models.

Retrieve relevant internal policies using Semantic Vector Search.

Audit the extracted data against the rules to identify violations and missing requirements.

🏗️ Architecture

The system utilizes the Google Agent Development Kit (ADK) pattern with a compliance_orchestrator managing three specialized sub-agents:

graph TD
    User[User Upload] -->|Contract/Invoice| Orch[Orchestrator Agent]
    
    subgraph "Agent Swarm"
        Orch -->|1. Vision Extraction| Parser[Robust Document Parser]
        Parser -->|Structured Markdown| Orch
        
        Orch -->|2. Query Rules| Retriever[Policy Retrieval Agent]
        Retriever -->|Fetch Context| VectorDB[(Policy Vector Store)]
        VectorDB -->|Relevant Clauses| Retriever
        
        Orch -->|3. Audit Logic| Checker[Discrepancy Checker]
        Checker -->|Violations & Citations| Orch
    end
    
    Orch -->|4. Final Report| Report[Compliance Audit Report]


The Agents

robust_document_parser: A Vision Agent (Gemini 1.5 Flash) capable of reading irregular tables and handwriting.

policy_retrieval_agent: A RAG-based agent that finds the specific policy rules relevant to the document's content.

discrepancy_checker: The auditor logic that compares Document Data vs. Policy Rules and flags non-compliance.

🚀 Key Features

Irregular Table Parsing: Handles merged cells, floating headers, and complex layouts that traditional OCR fails on.

Handwriting Recognition: accurately transcribes signatures and handwritten notes.

Citation-Based Auditing: Every flagged violation cites the specific policy section it violates.

Multi-Agent Coordination: Demonstrates sequential task delegation and loop-based retries for validation.

🛠️ Installation

Prerequisites

Python 3.9+

Google Gemini API Key

Setup

Clone the repository:

git clone [https://github.com/your-username/compliance-auditor.git](https://github.com/your-username/compliance-auditor.git)
cd compliance-auditor


Create a Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:

pip install -r requirements.txt


Set Environment Variables:
Create a .env file in the root directory:

GOOGLE_API_KEY=your_api_key_here


🏃 Usage

Place your policy documents (PDF/TXT) in data/policies/.

Place the document you want to audit in data/input_docs/.

Run the auditor:

python main.py


The system will initialize the vector store, process the document, and output a compliance report to the console (and data/reports/).

📂 Project Structure

compliance_auditor/
├── compliance_agent/           # Main Package
│   ├── orchestrator.py         # Main Manager Agent
│   ├── sub_agents/             # Specialist Agents
│   └── tools/                  # RAG & Reporting Tools
├── data/                       # Local Data Storage
│   ├── policies/               # Your Rulebooks
│   └── input_docs/             # Incoming Documents
├── main.py                     # Entry Point
└── requirements.txt            # Dependencies


📝 License

Apache 2.0