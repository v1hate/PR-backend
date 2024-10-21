import os
from flask import jsonify

UPLOAD_FOLDER = 'uploads/'

def save_file(file):
    """Guardar el archivo en la carpeta de uploads."""
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)  # Guardar el archivo
    return file_path

def list_files():
    """Devolver la lista de archivos subidos."""
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

def notify_users(connections, filename):
    """Notificar a los usuarios sobre un nuevo archivo."""
    for user_id in connections.keys():
        connections[user_id]['pending_files'].append(filename)

def get_pending_requests(user_id, pending_requests):
    """Obtener solicitudes pendientes para un usuario específico."""
    return {filename: user_id for user, filename in pending_requests.items() if user == user_id}
