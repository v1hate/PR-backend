from flask import Flask, request, jsonify
from flask_cors import CORS
import file_handler  # Importar el archivo con la lógica de manejo de archivos

app = Flask(__name__)
CORS(app)  # Permitir CORS para que el front-end pueda comunicarse con el back-end

@app.route('/devices', methods=['GET'])
def get_devices():
    """Obtener la lista de dispositivos en la red."""
    devices = file_handler.detect_devices()  # Llama a la función de detección de dispositivos
    return jsonify(devices)

@app.route('/send/<ip>', methods=['POST'])
def send_file(ip):
    """Enviar un archivo a un dispositivo específico."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Manejo del envío del archivo
    try:
        file_handler.send_file_to_device(ip, file)  # Llama a la función para enviar el archivo
        return jsonify({'message': 'File sent successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Ejecutar la aplicación en el puerto 5000
