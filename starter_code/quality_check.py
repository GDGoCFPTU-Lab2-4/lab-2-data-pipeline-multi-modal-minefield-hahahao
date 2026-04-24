# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    content = document_dict.get('content', '')
    
    # 1. Reject documents with 'content' length < 20 characters
    if len(content) < 20:
        print(f"Rejecting {document_dict.get('document_id')}: Content too short.")
        return False
        
    # 2. Reject documents containing toxic/error strings
    toxic_strings = ['Null pointer exception', 'Critical Error', 'Database connection failed']
    for ts in toxic_strings:
        if ts.lower() in content.lower():
            print(f"Rejecting {document_dict.get('document_id')}: Toxic content detected.")
            return False
            
    # 3. Flag discrepancies (Advanced)
    # Example: If it's code and has a mismatch (this is just a placeholder logic)
    if document_dict.get('source_type') == 'Code':
        if "8%" in content and "10%" in content: # Simulating discrepancy check
             print(f"Warning: Discrepancy detected in {document_dict.get('document_id')}")
    
    return True
