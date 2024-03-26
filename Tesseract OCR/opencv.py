import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\Thriveni\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'    
from PIL import Image

img = Image.open('WhatsApp Image 2024-03-12 at 10.49.23 AM.jpeg')
text = tess.image_to_string(img)

print(text)     