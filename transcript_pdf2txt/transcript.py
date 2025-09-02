import fitz

def get_json(pdf_path):    
    doc = fitz.open(pdf_path)
    document_data = []

    for page_num, page in enumerate(doc):
        page_data = {
            "page": page_num,
            "results": []
        }

        words = page.get_text("words")  # Returns: (x0, y0, x1, y1, "text", bloque_id)
        for word in words:
            x0, y0, x1, y1, text = word[:5]
            entry = {
                "text": text,
                "bbox": {
                    "x_min": int(x0),
                    "y_min": int(y0),
                    "x_max": int(x1),
                    "y_max": int(y1)
                }
            }
            page_data["results"].append(entry)

        document_data.append(page_data)

    return document_data



