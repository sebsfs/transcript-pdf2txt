import os
import argparse
from utils import read_json
from transcript_pdf2txt.transcript import get_json 
from transcript_pdf2txt.json2txt import generate_txt
from transcript_pdf2txt.transcript_ocr import paddleocr_to_json
from transcript_pdf2txt.legible import is_pdf_fully_legible

def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to TXT in order"
    )

    # Mandatory argument: input (PDF)
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="Path of the input PDF file"
    )

    # Optional argument: input (TXT)
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Path of the output TXT file (default: same name as the PDF)"
    )

    args = parser.parse_args()
    pdf_file = args.input

    # Convertion
    # With condition decide if use PyMuPDF (True) or PaddleOCR (False)
    if os.path.exists(pdf_file):
        condition = is_pdf_fully_legible(pdf_file)
        pdf_name, _ = os.path.splitext(pdf_file)

        # If the output directory is not specified → use the same name as the PD
        if args.output:
            output_file = args.output
        else:
            output_file = pdf_name + ".txt"

        if condition: # Digital PDF
            json_format = get_json(pdf_file) # PDF to json 
            generate_txt(json_format, output_file) # json to TXT

        else: # Scanned or encrypted PDF
            base, _ = os.path.splitext(pdf_file)
            output_json_path = base + ".json"
            # PDF to json
            paddleocr_to_json(pdf_file, output_json_path)
            json_format = read_json(output_json_path) # PDF to json 

            if os.path.exists(output_json_path):
                os.remove(output_json_path)

            generate_txt(json_format, output_file) # json to TXT

        print(f"PDF converted successfully: {output_file}")

    else:
        print('Enter a correct path')


if __name__ == "__main__":
    main()   