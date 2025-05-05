from PIL import Image
import os
from io import BytesIO

def save_user_photo(user_photo, user_id=None):
    # Lê a imagem do arquivo carregado pelo Streamlit
    image = Image.open(user_photo)
    
    # Converte a imagem em um formato de bytes para processamento em memória
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    
    # Retorna os dados da imagem em bytes para usar em outras funções
    return img_byte_arr
