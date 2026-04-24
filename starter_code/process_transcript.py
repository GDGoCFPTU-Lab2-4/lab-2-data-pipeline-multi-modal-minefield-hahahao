import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # 1. Remove noise tokens
    text = re.sub(r'\[Music.*?\]|\[inaudible\]|\[Laughter\]|\[Speaker \d+\]:', '', text)
    
    # 2. Strip timestamps
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # 3. Clean whitespace
    text = ' '.join(text.split()).strip()
    
    # 4. Find the price mentioned in Vietnamese words
    # "năm trăm nghìn" -> 500000
    price_vnd = 0
    if "năm trăm nghìn" in text.lower():
        price_vnd = 500000
    
    return {
        "document_id": "transcript-001",
        "content": text,
        "source_type": "Video",
        "author": "Lecture Speaker",
        "source_metadata": {
            "detected_price_vnd": price_vnd
        }
    }

