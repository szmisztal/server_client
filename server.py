from communication_utils import response_to_client
from network_utils import server_socket_create
from variables import HOST, PORT, BUFFER, utf8, server_start_time
from models import Command, User
from data_utils import serialize_json


server_socket = server_socket_create(HOST, PORT)
command = Command()
user = User("", "")

while True:
    client_socket, address = server_socket.accept()
    print(f"Connected from {HOST}:{PORT}")
    while True:
        client_request = client_socket.recv(BUFFER).decode(utf8)
        print(f"Client request: {client_request}")
        if client_request == "stop":
            break
        elif client_request == "uptime":
            response_data = response_to_client(client_request, command = command, server_start_time = server_start_time).encode(utf8)
            client_socket.send(response_data)
        elif client_request in ["info", "help", "logout"]:
            response_data = response_to_client(client_request, command = command).encode(utf8)
            client_socket.send(response_data)
        elif client_request == "register":
            registration_data = client_socket.recv(BUFFER).decode(utf8)
            response_data = response_to_client(client_request, registration_data = registration_data).encode(utf8)
            client_socket.send(response_data)
        elif client_request == "login":
            login_data = client_socket.recv(BUFFER).decode(utf8)
            response_data = response_to_client(client_request, user = user, login_data = login_data).encode(utf8)
            client_socket.send(response_data)
        elif client_request in ["show data", "inbox", "archived messages"]:
            response_data = response_to_client(client_request, user = user).encode(utf8)
            client_socket.send(response_data)
        elif client_request == "change data":
            new_data = client_socket.recv(BUFFER).decode(utf8)
            response_data = response_to_client(client_request, user = user, new_data = new_data).encode(utf8)
            client_socket.send(response_data)
        elif client_request == "send message":
            recipient_data = client_socket.recv(BUFFER).decode(utf8)
            response_data = response_to_client(client_request, recipient_data = recipient_data).encode(utf8)
            client_socket.send(response_data)
            message_data = client_socket.recv(BUFFER).decode(utf8)
            response_message = response_to_client(client_request, user = user, recipient_data = recipient_data, message_data = message_data).encode(utf8)
            client_socket.send(response_message)
        else:
            response_data = response_to_client(client_request).encode(utf8)
            client_socket.send(response_data)
    print(f"Connection from {HOST}:{PORT} closed")
    client_socket.close()
    server_socket.close()
    exit()


