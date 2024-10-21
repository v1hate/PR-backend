import os

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Almacena las solicitudes de envío de archivos
pending_requests = {}
# Almacena los usuarios conectados
connected_users = {}

def save_file(file, user_id):
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Agregar la solicitud de envío de archivo a la lista de solicitudes pendientes
        if user_id not in pending_requests:
            pending_requests[user_id] = []
        pending_requests[user_id].append(file.filename)

def get_uploaded_files():
    return os.listdir(UPLOAD_FOLDER)

def get_pending_requests(user_id):
    return pending_requests.get(user_id, {})

def accept_file(filename, user_id):
    if user_id in pending_requests:
        if filename in pending_requests[user_id]:
            pending_requests[user_id].remove(filename)
            return True
    return False

def connect_user(user_id):
    connected_users[user_id] = True

def disconnect_user(user_id):
    if user_id in connected_users:
        del connected_users[user_id]

def get_connected_users():
    return list(connected_users.keys())
