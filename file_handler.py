# backend/file_handler.py
import os

UPLOAD_FOLDER = 'uploads'

def save_file(file):
    """Guarda el archivo en el servidor y devuelve el nombre del archivo."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crea la carpeta si no existe
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return file.filename
