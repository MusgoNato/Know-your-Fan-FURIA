from PIL import Image
import pytesseract
import re
from io import BytesIO
import os

# Detecta se estamos em um ambiente local (Windows) ou em um ambiente de nuvem
if "TESSDATA_PREFIX" in os.environ:
    # Se estiver no Streamlit Cloud ou ambiente sem Tesseract instalado
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Caminho padrão do Tesseract no Linux (para Streamlit Cloud)
else:
    os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
    # Se estiver rodando localmente
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
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