from network_utils import server_socket_create
from variables import HOST, PORT, BUFFER, utf8
from models import Command

server_socket = server_socket_create(HOST, PORT)

while True:
    client_socket, address = server_socket.accept()
    print(f"Connected from {HOST}:{PORT}")
    while True:
        client_request = client_socket.recv(BUFFER).decode(utf8)
        if not client_request:
            break
        command = Command(client_request)
        print(f"Client request: {client_request}")
        if client_request == "stop":
            break
        else:
            response_data = command.response_to_client(client_request)
            client_socket.send(response_data)
    print("Server closed")
    client_socket.close()
    server_socket.close()
    exit()

