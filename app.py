from flask import Flask, request, jsonify
import file_handler
import socket

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Obtener la IP local del dispositivo para iniciar los servicios
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Se conecta a una IP externa pero no envía ningún dato
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# Ruta para obtener lista de dispositivos en la red
@app.route('/devices', methods=['GET'])
def list_devices():
    devices = file_handler.discover_devices()  # Uso de la detección automática de dispositivos
    return jsonify(devices)

# Ruta para enviar un archivo a un dispositivo específico
@app.route('/send/<ip>', methods=['POST'])
def send_file(ip):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    file_path = f"{app.config['UPLOAD_FOLDER']}/{file.filename}"
    file.save(file_path)
    
    # Enviar el archivo a través de TCP
    file_handler.send_file(ip, file_path)
    return jsonify({'message': 'Archivo enviado con éxito'})

# Ruta para listar archivos subidos
@app.route('/uploaded-files', methods=['GET'])
def uploaded_files():
    files = file_handler.list_uploaded_files(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

if __name__ == '__main__':
    # Obtener la IP local del dispositivo
    local_ip = get_local_ip()
    
    # Iniciar los servicios automáticos (detectar y recibir archivos)
    file_handler.start_device_services(local_ip, UPLOAD_FOLDER)
    
    app.run(host='0.0.0.0', port=5000)
