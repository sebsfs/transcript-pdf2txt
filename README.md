# Transcript-pdf2txt / PDF Text Extraction and Orientation Correction

This project provides an automated way to extract text from PDF documents while handling both digital and scanned files.  
The program ensures proper orientation and outputs clean, structured text.

## Features
- Detects if the PDF is digital (readable) or scanned.  
- Uses **PyMuPDF** for digital PDFs and **PaddleOCR** for scanned PDFs.  
- Corrects orientation issues by adjusting coordinates if the document is rotated.  
- Generates a **JSON file** containing transcription and word coordinates.  
- Produces a **TXT file** with words ordered to visually match the original PDF.

## Usage
```bash
python main.py -i "path/to/pdf/file" [-o "output/path/to/txt/file"]
```
- `-i` (required): Path to the input PDF file.  
- `-o` (optional): Path for the output TXT file. If not provided, the TXT will be saved in the same directory as the PDF with the same name.

## Output
- `output.txt`: Plain text file with words ordered to reflect the layout of the original document.

## Example
📄 Example with an invoice will be shown here (screenshots of results).
<p align="center">
  <img src="https://github.com/sebsfs/transcript-pdf2txt/blob/main/test_files/images/invoice_sample-1.jpg?raw=true" alt="Invoice sample" width="400"/>
  <img src="https://github.com/sebsfs/transcript-pdf2txt/blob/main/test_files/images/output_transcript.png?raw=true" alt="Output transcript" width="400"/>
</p>
---
