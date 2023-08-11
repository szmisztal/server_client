import socket as s

HOST = "127.0.0.1"
PORT = 65432

client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
client_socket.connect((HOST, PORT))


