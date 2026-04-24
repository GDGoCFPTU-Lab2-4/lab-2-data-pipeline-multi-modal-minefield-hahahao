import ast

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    tree = ast.parse(source_code)
    docstrings = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            ds = ast.get_docstring(node)
            if ds:
                name = getattr(node, 'name', 'Module')
                docstrings.append(f"{name}: {ds}")
                
    content = "\n".join(docstrings)
    
    # Advanced: Extract comments starting with "# Business Logic Rule"
    rules = []
    for line in source_code.split('\n'):
        if "# Business Logic Rule" in line:
            rules.append(line.split("#")[-1].strip())
    
    return {
        "document_id": "legacy-code-001",
        "content": content,
        "source_type": "Code",
        "author": "Legacy System",
        "source_metadata": {
            "functions_found": len([d for d in docstrings if ':' in d]),
            "business_rules": rules
        }
    }

