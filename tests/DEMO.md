🧪 Testing & Demo Guide

This document explains how to verify the Autonomous Compliance Auditor and what the successful output looks like.

1. How to Run the Test

We have included a dedicated test suite that verifies if the Agent correctly identifies the 3 deliberate violations in the Vendor_Service_Agreement.txt.

Command:

python3 tests/test_agent.py


2. Expected Output

When you run the main application or the test suite, you should see the following logs demonstrating the Multi-Agent Workflow:

Agent Stages

Vision Agent: Ingests the file (simulated upload) and extracts text.

Retrieval Agent: Analyzes the text -> Queries Vector DB -> Finds "Procurement Policy".

Auditor Agent: Compares "Net 90 Days" (Contract) vs "Net 45 Days" (Policy).

Sample Terminal Output

(Your specific wording may vary slightly as the AI generates it freshly each time)

--- Autonomous Compliance Auditor Starting ---
[*] Orchestrator: Initializing Agents...
[*] Ingesting policies from data/policies/...
[*] Successfully indexed 5 policy chunks.

[*] Starting Audit for: data/input_docs/Vendor_Service_Agreement.txt

--- Step 1: Parsing Document (Vendor_Service_Agreement.txt) ---
[*] Parser Agent: Uploading data/input_docs/Vendor_Service_Agreement.txt...
[*] Extraction Complete.

--- Step 2: Retrieving Policies ---
[*] Policy Retrieval Agent: Analyzing document...
[*] Generated Queries: ['Payment Terms', 'Liability Cap', 'Governing Law']
[*] Searching Vector DB...

--- Step 3: Auditing Discrepancies ---
[*] Discrepancy Checker: Running audit logic...

==================================================
FINAL COMPLIANCE REPORT
==================================================
# Compliance Audit Report
**Compliance Score:** 40/100

## Detailed Findings
### Violation 1
- **Issue:** Payment Terms exceed limit
- **Policy Reference:** "Under no circumstances shall payment terms exceed 90 days." (Standard is 45)
- **Document Text:** "Client shall pay all undisputed invoices within Net 90 days"
- **Severity:** High

### Violation 2
- **Issue:** Liability Cap insufficient
- **Policy Reference:** "Liability shall not be limited to less than 2x contract value or $1,000,000"
- **Document Text:** "Limited to fees paid in preceding 3 months (approx $37,500)"
- **Severity:** High

### Violation 3
- **Issue:** Incorrect Governing Law
- **Policy Reference:** "Must be governed by laws of New York"
- **Document Text:** "Governed by the laws of the State of California"
- **Severity:** Medium
==================================================


3. Verification Checklist

[x] Import Success: All modules (google-generativeai, chromadb) loaded.

[x] Vector Store: Policy document was indexed successfully.

[x] Vision: Document text was extracted.

[x] Logic: The "Net 90 Days" violation was flagged.