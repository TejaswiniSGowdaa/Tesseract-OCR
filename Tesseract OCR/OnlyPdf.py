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

if  __name__ == "__main__":
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
    
    # Save extracted texts as JSON
    with open("extracted_texts.json", "w") as json_file:
        json.dump(extracted_texts, json_file, indent=4)
    print("Extracted texts saved to 'extracted_texts.json'")
