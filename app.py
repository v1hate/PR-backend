from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from file_handler import save_file  
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

connected_users = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    return handle_file_upload()

@socketio.on('connect_user')
def handle_connect(data):
    return handle_user_connection(data['user_id'])

@socketio.on('disconnect')
def handle_disconnect():
    return handle_user_disconnection()

# Función para manejar la carga de archivos
def handle_file_upload():
    file = request.files['file']
    user_id = request.form['user_id']
    filename = save_file(file)

    # Emitir evento a todos los usuarios sobre la carga del archivo
    socketio.emit('file_uploaded', {'filename': filename, 'user_id': user_id})
    
    return {'status': 'success', 'filename': filename}

# Función para manejar la conexión de usuarios
def handle_user_connection(user_id):
    connected_users[user_id] = request.sid
    emit('user_list', list(connected_users.keys()), broadcast=True)

# Función para manejar la desconexión de usuarios
def handle_user_disconnection():
    user_id = next((uid for uid, sid in connected_users.items() if sid == request.sid), None)
    if user_id:
        del connected_users[user_id]
        # Emitir la lista de usuarios actualizada
        socketio.emit('user_list', list(connected_users.keys()))

if __name__ == '__main__':
    socketio.run(app)
