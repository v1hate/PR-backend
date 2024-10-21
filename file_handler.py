import socket
import os

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear la carpeta de uploads si no existe

def detect_devices():
    """Detecta dispositivos en la red local utilizando UDP."""
    devices = []
    broadcast_address = '<broadcast>'
    port = 5005

    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)

    # Enviar un mensaje de broadcast para detectar dispositivos
    message = "¿Hay alguien ahí?"
    print("Enviando mensaje de broadcast...")
    sock.sendto(message, (broadcast_address, port))

    time.sleep(1)  # Esperar un segundo antes de empezar a recibir respuestas

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Dispositivo detectado: {data.decode()} en {addr[0]}")
            devices.append({'name': data.decode(), 'ip': addr[0]})
    except socket.timeout:
        print("Tiempo de espera alcanzado. Finalizando detección.")

    sock.close()
    print(f"Dispositivos encontrados: {devices}")
    return devices


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
