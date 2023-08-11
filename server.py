import socket as s

HOST = "127.0.0.1"
PORT = 65432

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

while True:
    client_socket, address = server_socket.accept()
    print(f"You have connection from {address[0]}:{address[1]}")
