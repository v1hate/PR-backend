import socket
import os
import threading

# Función para enviar un mensaje de broadcast UDP para detectar dispositivos
def discover_devices(broadcast_port=9000, timeout=5):
    discovered_devices = []

    # Crear un socket UDP para enviar el mensaje de broadcast
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(timeout)

    # Mensaje de broadcast
    message = b'DISCOVER_DEVICE'
    s.sendto(message, ('<broadcast>', broadcast_port))

    try:
        while True:
            # Recibir respuestas de los dispositivos
            data, addr = s.recvfrom(1024)
            if data.decode() == 'DEVICE_RESPONSE':
                discovered_devices.append({"ip": addr[0], "name": addr[0]})
    except socket.timeout:
        pass
    finally:
        s.close()

    return discovered_devices

# Servidor UDP que responde a los mensajes de broadcast (este proceso será automático en cada dispositivo)
def start_broadcast_listener(ip, broadcast_port=9000):
    def listen():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((ip, broadcast_port))
        
        while True:
            data, addr = s.recvfrom(1024)
            if data == b'DISCOVER_DEVICE':
                s.sendto(b'DEVICE_RESPONSE', addr)
                
    thread = threading.Thread(target=listen)
    thread.daemon = True  # Hilo en segundo plano
    thread.start()

# Función para enviar archivo a través de TCP
def send_file(ip, file_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, 9001))
        file_name = os.path.basename(file_path)
        s.send(file_name.encode())

        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                s.send(data)
                data = file.read(1024)
    finally:
        s.close()

# Función para listar los archivos subidos
def list_uploaded_files(upload_folder):
    return os.listdir(upload_folder)

# Servidor TCP para recibir archivos (inicia automáticamente)
def start_file_server(ip, port, save_folder):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        file_name = conn.recv(1024).decode()
        file_path = os.path.join(save_folder, file_name)

        with open(file_path, 'wb') as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
        conn.close()

# Inicia automáticamente la escucha de broadcast y servidor de archivos en el dispositivo
def start_device_services(ip, save_folder):
    start_broadcast_listener(ip)  # Detecta automáticamente los mensajes de otros dispositivos
    start_file_server(ip, 9001, save_folder)  # Inicia automáticamente el servidor TCP para recibir archivos
