from PIL import Image
import pytesseract
import re
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

def extract_textFromImg(path):
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang='por')
    return text

def extract_cpfFromText(text):
    pattern = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'
    valid_cpf = re.findall(pattern, text)
    return valid_cpf