from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    table = soup.find('table', id='main-catalog')
    if not table:
        return []
    
    results = []
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
            
        sp_id = cols[0].get_text(strip=True)
        name = cols[1].get_text(strip=True)
        category = cols[2].get_text(strip=True)
        price_raw = cols[3].get_text(strip=True)
        stock = cols[4].get_text(strip=True)
        rating = cols[5].get_text(strip=True)
        
        # Clean price
        price_val = 0.0
        if price_raw not in ['N/A', 'Liên hệ']:
            # Extract number from "28,500,000 VND"
            price_str = price_raw.replace('VND', '').replace(',', '').replace('.', '').strip()
            try:
                price_val = float(price_str)
            except ValueError:
                price_val = 0.0
        
        doc = {
            "document_id": f"html-{sp_id}",
            "content": f"Product {name} in {category}. Price: {price_raw}. Rating: {rating}.",
            "source_type": "HTML",
            "author": "VinShop System",
            "source_metadata": {
                "product_id": sp_id,
                "price_numeric": price_val,
                "stock": int(stock) if stock.isdigit() or (stock.startswith('-') and stock[1:].isdigit()) else 0,
                "rating": rating
            }
        }
        results.append(doc)
    
    return results

