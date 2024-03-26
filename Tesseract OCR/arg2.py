import pytesseract as tess
from PIL import Image
import sys
import json

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = tess.image_to_string(img)
        return {"image": image_path, "text": text}
    except Exception as e:
        return {"image": image_path, "error": str(e)}

if __name__ == "__main__":
    tess.pytesseract.tesseract_cmd = r'C:\Users\Thriveni\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    
    if len(sys.argv) < 2:
        print(r"C:\Users\Thriveni\OneDrive\Desktop\ImageToText\tej.jpg")
        sys.exit(1)
                
    extracted_texts = []
    for image_path in sys.argv[1:]:
        print("Processing image:", image_path)
        extracted_text = extract_text_from_image(image_path)
        extracted_texts.append(extracted_text)
        print("Text extracted from the image:")
        print(extracted_text)
        print("-----------------------------")
    
    # Save extracted texts as JSON
    with open("extracted_texts.json", "w") as json_file:
        json.dump(extracted_texts, json_file, indent=4)
    print("Extracted texts saved to 'extracted_texts.json'")

