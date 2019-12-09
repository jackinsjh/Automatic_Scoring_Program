from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\sohnj\Documents\Tesseract-OCR\tesseract.exe'

ocrFile = 'ocrTest1.jpg'
im = Image.open(ocrFile)
text = pytesseract.image_to_string(im)
print(text)


