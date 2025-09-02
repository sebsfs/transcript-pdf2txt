############## Filter to determine the extraction method ##############
import string
import fitz

def is_text_legible(text):
    printable = set(string.printable)
    if not text.strip():
        return False
    num_printable = sum(1 for c in text if c in printable)
    legibility_ratio = num_printable / len(text)
    return legibility_ratio > 0.7

def is_pdf_fully_legible(pdf_path):
    doc = fitz.open(pdf_path)
    for page_num, page in enumerate(doc, start=1):
        # Detect if the page has text blocks
        blocks = page.get_text("dict")["blocks"]
        text_blocks = [b for b in blocks if "lines" in b]

        text = page.get_text()
        if not text_blocks or not is_text_legible(text):
            print(f"Page {page_num} appears scanned or encrypted.")
            return False  # Page probably scanned

    return True  # All pages have legible text
