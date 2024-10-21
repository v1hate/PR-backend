# backend/file_handler.py
import os

UPLOAD_FOLDER = 'uploads'

def save_file(file):
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    return filename

def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
