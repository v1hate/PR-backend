# backend/app.py
from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from file_handler import save_file, delete_file  
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

connected_users = {}
uploaded_files = []  # Lista para almacenar archivos subidos

UPLOAD_FOLDER = 'uploads'  # Carpeta donde se guardan los archivos
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear la carpeta si no existe

@app.route('/upload', methods=['POST'])
def upload_file():
    return handle_file_upload()

@app.route('/files/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file_route(filename):
    return handle_file_deletion(filename)

@socketio.on('connect_user')
def handle_connect(data):
    handle_user_connection(data['user_id'])

@socketio.on('disconnect')
def handle_disconnect():
    handle_user_disconnection()

# Función para manejar la carga de archivos
def handle_file_upload():
    file = request.files['file']
    user_id = request.form['user_id']

    # Guardar el archivo
    filename = save_file(file)
    if filename:
        uploaded_files.append(filename)  # Agregar archivo a la lista de archivos subidos

        # Emitir evento a todos los usuarios sobre la carga del archivo
        socketio.emit('file_uploaded', {'filename': filename, 'user_id': user_id})

        # Emitir la lista de archivos a todos los usuarios
        socketio.emit('update_file_list', uploaded_files)

        return {'status': 'success', 'filename': filename}
    return {'status': 'error', 'message': 'Failed to save file'}

# Función para manejar la eliminación de archivos
def handle_file_deletion(filename):
    if delete_file(filename):
        uploaded_files.remove(filename)  # Eliminar archivo de la lista
        socketio.emit('update_file_list', uploaded_files)  # Emitir la lista actualizada
        return {'status': 'success'}
    return {'status': 'error', 'message': 'File not found'}

# Función para manejar la conexión de usuarios
def handle_user_connection(user_id):
    connected_users[user_id] = request.sid
    emit('user_list', list(connected_users.keys()), broadcast=True)  # Emitir lista de usuarios conectados

# Función para manejar la desconexión de usuarios
def handle_user_disconnection():
    user_id = next((uid for uid, sid in connected_users.items() if sid == request.sid), None)
    if user_id:
        del connected_users[user_id]
        # Emitir la lista de usuarios actualizada
        socketio.emit('user_list', list(connected_users.keys()))
        # Emitir la lista de archivos a los usuarios restantes
        socketio.emit('update_file_list', uploaded_files)

if __name__ == '__main__':
    socketio.run(app)
