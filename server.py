from communication_utils import response_to_client
from network_utils import server_socket_create
from models import Command
from variables import HOST, PORT, BUFFER, utf8, server_start_time


server_socket = server_socket_create(HOST, PORT)
command = Command()

while True:
    client_socket, address = server_socket.accept()
    print(f"Connected from {HOST}:{PORT}")
    while True:
        client_request = client_socket.recv(BUFFER).decode(utf8)
        if not client_request:
            break
        print(f"Client request: {client_request}")
        if client_request == "stop":
            break
        elif client_request == "register":
            registration_data = client_socket.recv(BUFFER).decode(utf8)
            response_data = response_to_client(client_request, registration_data = registration_data).encode(utf8)
        else:
            response_data = response_to_client(client_request, command = command, server_start_time = server_start_time).encode(utf8)
        client_socket.send(response_data)
    print(f"Connection from {HOST}:{PORT} closed")
    client_socket.close()
    server_socket.close()
    exit()


