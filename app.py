# backend/app.py
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from file_handler import save_file  # Importa la función save_file
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

connected_users = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    user_id = request.form['user_id']
    filename = save_file(file)  # Usa la función save_file
    socketio.emit('file_uploaded', {'filename': filename, 'user_id': user_id})
    return {'status': 'success'}

@socketio.on('connect')
def handle_connect():
    user_id = request.args.get('user_id')
    connected_users[user_id] = request.sid
    socketio.emit('user_list', list(connected_users.keys()))

@socketio.on('disconnect')
def handle_disconnect():
    user_id = next((uid for uid, sid in connected_users.items() if sid == request.sid), None)
    if user_id:
        del connected_users[user_id]
        socketio.emit('user_list', list(connected_users.keys()))

if __name__ == '__main__':
    socketio.run(app)
