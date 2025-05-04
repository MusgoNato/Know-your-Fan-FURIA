import os

def save_user_photo(user_photo, user_id):
    """Retorna o caminho da foto"""
    if user_photo is not None:
        folder = "./assets/user"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"user_{user_id}.png")
        with open(file_path, "wb") as f:
            f.write(user_photo.getbuffer())
        return file_path
    return None
