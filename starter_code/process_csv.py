import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # 1. Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset=['id'], keep='first')
    
    # 2. Clean 'price' column
    def clean_price(val):
        if pd.isna(val) or val in ['N/A', 'NULL', 'Liên hệ']:
            return 0.0
        val = str(val).lower().replace('$', '').replace(',', '')
        if 'five dollars' in val:
            return 5.0
        try:
            return float(val)
        except ValueError:
            return 0.0

    df['price'] = df['price'].apply(clean_price)
    
    # 3. Normalize 'date_of_sale'
    # pd.to_datetime is quite smart, but let's be careful with format variations
    df['date_of_sale'] = pd.to_datetime(df['date_of_sale'], errors='coerce')
    
    # 4. Convert to UnifiedDocument list
    results = []
    for _, row in df.iterrows():
        doc = {
            "document_id": f"csv-{row['id']}",
            "content": f"Product: {row['product_name']}, Category: {row['category']}, Price: {row['price']} {row['currency']}",
            "source_type": "CSV",
            "author": f"Seller {row['seller_id']}",
            "timestamp": row['date_of_sale'].isoformat() if not pd.isna(row['date_of_sale']) else None,
            "source_metadata": {
                "product_name": row['product_name'],
                "category": row['category'],
                "price": float(row['price']),
                "currency": row['currency'],
                "stock_quantity": row['stock_quantity'] if not pd.isna(row['stock_quantity']) else 0
            }
        }
        results.append(doc)
    
    return results

