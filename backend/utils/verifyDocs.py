from PIL import Image
import pytesseract
import re
from io import BytesIO
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

def extract_textFromImg(image_bytes):
    # Converte os bytes da imagem de volta para um objeto Image
    image = Image.open(BytesIO(image_bytes))
    
    # Processa a imagem com o pytesseract
    text = pytesseract.image_to_string(image)
    
    return text

def extract_cpfFromText(text):
    pattern = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'
    valid_cpf = re.findall(pattern, text)
    return valid_cpf