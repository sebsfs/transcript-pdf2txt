import os 
import json
import shutil
from paddleocr import PaddleOCR

def convert_paddleocr_to_page_format(data, page_index):
    texts = data.get("rec_texts", [])
    boxes = data.get("rec_boxes", [])

    results = []
    for text, box in zip(texts, boxes):
        if len(box) == 4:
            result = {
                "text": text,
                "bbox": {
                    "x_min": int(box[0]),
                    "y_min": int(box[1]),
                    "x_max": int(box[2]),
                    "y_max": int(box[3])
                }
            }
            results.append(result)

    return {
        "page": page_index,
        "results": results
    }

def paddleocr_to_json(pdf_path, output_json_path):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False)

    # Run OCR inference on a sample image 
    result = ocr.predict(
        input = pdf_path)

    # Visualize the results and save the JSON results
    base_path = os.path.dirname(pdf_path)
    for res in result:
        res.save_to_json(f"{base_path}/temp")  

    # Assume the files are named file_0_res.json, file_1_res.json, ...
    combined_pages = []

    # Traverse sequentially while files exist
    page_index = 0
    while True:
        filename2 = f"{filename}_{page_index}_res.json"
        file_path = os.path.join(f"{base_path}/temp", filename2)
        if not os.path.exists(file_path):
            break  # Ya no hay más páginas

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            page_data = convert_paddleocr_to_page_format(data, page_index)
            combined_pages.append(page_data)

        page_index += 1

    # write combined JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(combined_pages, f, ensure_ascii=False, indent=2)

    print(f"Transcript was generated: {output_json_path}")
    shutil.rmtree(f"{base_path}/temp")
