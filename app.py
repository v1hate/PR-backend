from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from file_handler import save_file, list_files, notify_users

app = Flask(__name__)
CORS(app)

# Mantener la lista de conexiones activas
connections = {}
pending_requests = {}  # Solicitudes pendientes de archivos

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filepath = save_file(file)  # Usar función para guardar el archivo

    # Notificar a todos los usuarios conectados que hay un archivo disponible
    notify_users(connections, file.filename)
    
    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/files', methods=['GET'])
def get_files():
    """Devolver la lista de archivos subidos."""
    return list_files()

@app.route('/connect', methods=['POST'])
def connect_user():
    """Conectar un usuario al servidor."""
    user_id = request.json.get('user_id')
    if user_id:
        connections[user_id] = {'ip': request.remote_addr, 'pending_files': []}  # Guardar IP y lista de archivos pendientes
        return jsonify({'message': 'User connected successfully'}), 200
    return jsonify({'error': 'No user ID provided'}), 400

@app.route('/accept', methods=['POST'])
def accept_file():
    """Aceptar recibir un archivo."""
    user_id = request.json.get('user_id')
    if user_id in pending_requests:
        filename = pending_requests[user_id]
        # Aquí deberías implementar la lógica para enviar el archivo al usuario
        del pending_requests[user_id]  # Eliminar la solicitud después de aceptarla
        return jsonify({'message': f'File {filename} will be sent to {user_id}'}), 200
    return jsonify({'error': 'No pending requests for this user'}), 400

@app.route('/pending-requests', methods=['GET'])
def get_pending_requests():
    """Obtener las solicitudes pendientes para el usuario actual."""
    user_id = request.args.get('user_id')
    requests = {filename: user_id for user, filename in pending_requests.items() if user == user_id}
    return jsonify(requests)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Crear la carpeta si no existe
    app.run(host='0.0.0.0', port=5000)
