import socket as s
from server_response import server_response

HOST = "127.0.0.1"
PORT = 65432

BUFFER = 1024

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

while True:
    client_socket, address = server_socket.accept()
    print(f"You have connection from {address[0]}:{address[1]}")
    msg = "Commands: uptime / info / help / stop".encode("utf8")
    client_socket.send(msg)
    client_request = client_socket.recv(BUFFER).decode("utf8")
    server_answer = server_response(client_request).encode("utf8")
    client_socket.send(server_answer)
    if client_request == "stop":
        "Server is shutting down"
        break
