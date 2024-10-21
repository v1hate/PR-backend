from flask import Flask, request, jsonify
from flask_cors import CORS
from file_handler import save_file, get_uploaded_files, get_pending_requests, accept_file

app = Flask(__name__)
CORS(app)  # Permitir CORS

# Ruta para conectar un usuario
@app.route('/connect', methods=['POST'])
def connect_user():
    data = request.get_json()
    user_id = data.get('user_id')

    # Aquí podrías añadir lógica adicional para gestionar conexiones
    return jsonify({'message': f'Usuario {user_id} conectado exitosamente.'})

# Ruta para subir un archivo
@app.route('/upload', methods=['POST'])
def upload_file():
    user_id = request.form['user_id']
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    save_file(file, user_id)

    return jsonify({'message': f'Archivo {file.filename} subido exitosamente.'})

# Ruta para obtener archivos subidos
@app.route('/files', methods=['GET'])
def files():
    uploaded_files = get_uploaded_files()
    return jsonify(uploaded_files)

# Ruta para obtener solicitudes pendientes
@app.route('/pending-requests', methods=['GET'])
def pending_requests():
    user_id = request.args.get('user_id')
    requests = get_pending_requests(user_id)
    return jsonify(requests)

# Ruta para aceptar un archivo
@app.route('/accept', methods=['POST'])
def accept():
    data = request.get_json()
    user_id = data.get('user_id')
    filename = data.get('filename')

    if accept_file(filename, user_id):
        return jsonify({'message': f'Archivo {filename} aceptado.'})
    else:
        return jsonify({'message': 'Error al aceptar el archivo.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
