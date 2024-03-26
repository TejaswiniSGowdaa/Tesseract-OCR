import pytesseract as tess
from pdf2image import convert_from_path
import sys
import json
import re

# GSTIN regular expression 
gstinRegex = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z0-9]{2}[Z][A-Z0-9]$"

def validate_gstin(text):
    # Check if text matches GSTIN regex
    return re.match(gstinRegex, text) is not None

def extract_text_from_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        extracted_texts = []
        for i, img in enumerate(images):
            text = tess.image_to_string(img)
            gstin_match = validate_gstin(text)
            extracted_texts.append({"page": i+1, "text": text, "gstin_valid": gstin_match})
        return extracted_texts  
    
    except Exception as e:
        return {"pdf": pdf_path, "error": str(e)}

def extract_lines_and_rows_from_text(text, line_numbers, row_numbers):
    lines = text.split('\n')
    extracted_data = {}
    
    for line_number in line_numbers:
        if 0 < line_number <= len(lines):
            extracted_line = lines[line_number - 1]
            extracted_data[line_number] = {}
            for row_number in row_numbers:
                if 0 < row_number <= len(extracted_line.split()):
                    extracted_data[line_number][row_number] = extracted_line.split()[row_number - 1]
        else:
            extracted_data[line_number] = None
    
    return extracted_data

if __name__ == "__main__":
    tess.pytesseract.tesseract_cmd = r'C:\Users\Thriveni\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    print("Usage: python script.py path/to/your/pdf.pdf")
    if len(sys.argv) < 2:
        print("Usage: python script.py path/to/your/pdf.pdf")
        sys.exit(1)
        
    pdf_path = sys.argv[1]
    
    print("Processing PDF:", pdf_path)
    extracted_texts = extract_text_from_pdf(pdf_path)
    
    print("Text extracted from the PDF:")
    for text in extracted_texts:
        print("Page:", text["page"])
        print("Text:", text["text"])
        print("GSTIN Valid:", text["gstin_valid"])
        print("-----------------------------")
        
        line_numbers = [6]  # Line numbers to extract
        row_numbers = [1, 2, 4, 6]  # Row numbers to extract
        
        extracted_data = extract_lines_and_rows_from_text(text["text"], line_numbers, row_numbers)
        for line_number, data in extracted_data.items():
            if data:
                print("Extracted Line {} from Page {}: {}".format(line_number, text["page"], data))
            else:
                print("Line {} not found in Page {}".format(line_number, text["page"]))
        print("-----------------------------")  


