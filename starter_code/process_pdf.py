import google.generativeai as genai
import os

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Use Gemini API to extract structured data from lecture_notes.pdf

def extract_pdf_data(file_path):
    # --- FILE CHECK (Handled for students) ---
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    # ------------------------------------------

    # Initialize Gemini API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Warning: GOOGLE_API_KEY not found. Skipping PDF processing or using mock data.")
        # Mock data for demonstration if key is missing
        return {
            "document_id": "pdf-mock-001",
            "content": "This is a mock summary of the lecture notes because GOOGLE_API_KEY was not provided.",
            "source_type": "PDF",
            "author": "Mock Author",
            "source_metadata": {"status": "mocked"}
        }

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        # Upload the file
        pdf_file = genai.upload_file(path=file_path)
        
        # Send a prompt to Gemini
        response = model.generate_content([
            pdf_file, 
            "Extract the following information from this PDF and return as JSON: Title, Author, and a 3-sentence summary."
        ])
        
        # In a real scenario, we'd parse the JSON. Here we'll just take the text.
        content_text = response.text
        
        return {
            "document_id": "pdf-lecture-notes",
            "content": content_text,
            "source_type": "PDF",
            "author": "Dr. VinAI", # Example author
            "source_metadata": {
                "file_name": os.path.basename(file_path),
                "model_used": "gemini-1.5-flash"
            }
        }
    except Exception as e:
        print(f"Error during Gemini processing: {e}")
        return None
