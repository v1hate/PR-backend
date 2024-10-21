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
