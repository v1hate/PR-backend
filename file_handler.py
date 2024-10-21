# backend/file_handler.py
import os

UPLOAD_FOLDER = 'uploads'  # Carpeta donde se guardarán los archivos

# Asegúrate de que la carpeta existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_file(file):
    # Guarda el archivo y devuelve el nombre del archivo guardado
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    return filename

def delete_file(filename):
    # Elimina el archivo si existe y devuelve True o False
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
