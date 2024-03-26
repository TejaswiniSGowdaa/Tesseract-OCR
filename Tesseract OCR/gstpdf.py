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
        extracted_info = {
            "Registration Number": "",
            "Legal Name": "",
            "Trade Name, if any ": "",
            "Address of Principal Place of Business": "",
            "Period of Validity": ""
        }
        
        for img in images:
            text = tess.image_to_string(img)
            lines = text.split("\n")
            for line in lines:
                # Extracting Registration Number
                if "Registration Number" in line:
                    extracted_info["Registration Number"] = re.findall(r'\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}\b', line)[0]
                # Extracting Legal Name
                elif "Legal Name" in line:
                    extracted_info["Legal Name"] = line.split("Legal Name")[-1].strip()
                # Extracting Trade Name
                elif "Trade Name, if any " in line:
                    extracted_info["Trade Name, if any "] = line.split("Trade Name, if any ")[-1].strip()
                # Extracting Address of Principal Place of
                elif "Address of Principal Place of" in line:
                    address_line1 = line.split("Address of Principal Place of")[1].strip()
                    # Check the next line for "Business"
                    next_line = lines[lines.index(line) + 1]
                    if "Business" in next_line:
                        address_line2 = next_line.split("Business")[1].strip()
                        extracted_info["Address of Principal Place of Business"] = address_line1 + " " + address_line2
                    else:
                        extracted_info["Address of Principal Place of Business"] = address_line1
                # Extracting Period of Validity
                elif "Period of Validity" in line:
                    extracted_info["Period of Validity"] = line.split("Period of Validity")[-1].strip()        
                    
        return extracted_info
    
    except Exception as e:
        return {"pdf": pdf_path, "error": str(e)}

if __name__ == "__main__":
    tess.pytesseract.tesseract_cmd = r'C:\Users\Thriveni\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    print("Usage: python script.py path/to/your/pdf.pdf")
    if len(sys.argv) < 2:
        print("Usage: python script.py path/to/your/pdf.pdf")
        sys.exit(1)
        
    pdf_path = sys.argv[1]
    
    print("Processing PDF:", pdf_path)
    extracted_info = extract_text_from_pdf(pdf_path)
    
    print("Extracted Information:")
    print(json.dumps(extracted_info, indent=4))
    
    # Save extracted information as JSON
    with open("extracted_information.json", "w") as json_file:
        json.dump(extracted_info, json_file, indent=4)
    print("Extracted information saved to 'extracted_information.json'")
    
    # Validate extracted GSTIN
    gstin_validity = validate_gstin(extracted_info["Registration Number"])
    print("GSTIN Validity:", gstin_validity)
