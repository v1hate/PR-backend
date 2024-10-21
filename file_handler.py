import socket
import os

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear la carpeta de uploads si no existe

def detect_devices():
    """Detecta dispositivos en la red local utilizando UDP."""
    devices = []
    broadcast_address = '<broadcast>'  # Dirección de broadcast
    port = 5005  # Puerto a utilizar para el broadcast

    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Permitir broadcast
    sock.settimeout(2)  # Tiempo de espera para las respuestas

    # Enviar un mensaje de broadcast para detectar dispositivos
    message = "¿Hay alguien ahí?"
    sock.sendto(message, (broadcast_address, port))

    try:
        while True:
            # Escuchar respuestas de dispositivos
            data, addr = sock.recvfrom(1024)  # Tamaño del buffer de recepción
            devices.append({'name': data.decode(), 'ip': addr[0]})  # Añadir dispositivo detectado
    except socket.timeout:
        pass  # Fin de la detección

    sock.close()
    return devices  # Retornar la lista de dispositivos detectados

def send_file_to_device(ip, file):
    """Envía un archivo a un dispositivo específico utilizando TCP."""
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)  # Guardar el archivo en la carpeta uploads
    file.save(save_path)  # Guardar el archivo en el servidor

    # Configuración del socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, 5006))  # Conectar al dispositivo en el puerto 5006
        with open(save_path, 'rb') as f:
            data = f.read(1024)
            while data:
                s.sendall(data)  # Enviar el archivo en bloques de 1024 bytes
                data = f.read(1024)

    print(f"Archivo {file.filename} enviado a {ip}.")  # Mensaje de confirmación
