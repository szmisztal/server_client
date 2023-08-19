import socket as s


def server_socket_create(HOST, PORT):
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    return server_socket

def client_socket_create(HOST, PORT):
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    return client_socket
