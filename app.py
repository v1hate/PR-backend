from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
from file_handler import (
    save_file,
    get_uploaded_files,
    get_pending_requests,
    accept_file,
    connect_user,
    disconnect_user,
    get_connected_users
)
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

UPLOAD_FOLDER = 'uploads'

@app.route('/connect', methods=['POST'])
def connect_user_route():
    data = request.get_json()
    user_id = data.get('user_id')

    if user_id in get_connected_users():
        return jsonify({'message': 'Ya existe un usuario con ese ID conectado.'}), 400

    connect_user(user_id)
    socketio.emit('update_users', get_connected_users())  # Emitir la actualización de usuarios
    return jsonify({'message': f'Usuario {user_id} conectado exitosamente.'})

@app.route('/disconnect', methods=['POST'])
def disconnect_user_route():
    data = request.get_json()
    user_id = data.get('user_id')
    disconnect_user(user_id)
    socketio.emit('update_users', get_connected_users())  # Emitir la actualización de usuarios
    return jsonify({'message': f'Usuario {user_id} desconectado exitosamente.'})

@app.route('/upload', methods=['POST'])
def upload_file():
    user_id = request.form['user_id']
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    save_file(file, user_id)
    socketio.emit('update_files', get_uploaded_files())  # Emitir la actualización de archivos
    return jsonify({'message': f'Archivo {file.filename} subido exitosamente.'})

@app.route('/files', methods=['GET'])
def files():
    uploaded_files = get_uploaded_files()
    return jsonify(uploaded_files)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/pending-requests', methods=['GET'])
def pending_requests_route():
    user_id = request.args.get('user_id')
    requests = get_pending_requests(user_id)
    return jsonify(requests)

@app.route('/accept', methods=['POST'])
def accept_route():
    data = request.get_json()
    user_id = data.get('user_id')
    filename = data.get('filename')

    if accept_file(filename, user_id):
        return jsonify({'message': f'Archivo {filename} aceptado.'})
    else:
        return jsonify({'message': 'Error al aceptar el archivo.'}), 400

@socketio.on('connect')
def handle_connect():
    print("Cliente conectado")

@socketio.on('disconnect')
def handle_disconnect():
    print("Cliente desconectado")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
