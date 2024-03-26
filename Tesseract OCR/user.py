import pytesseract as tess
from PIL import Image


tess.pytesseract.tesseract_cmd = r'C:\Users\Thriveni\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
image_path = input("Enter the path of the image file: ")

try:
    img = Image.open(image_path)
    text = tess.image_to_string(img)
    print("Text extracted from the image:")
    print(text)

except Exception as e:
    print("An error occurred:", e) 
