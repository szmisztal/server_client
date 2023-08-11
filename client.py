import socket as s

HOST = "127.0.0.1"
PORT = 65432

BUFFER = 1024

client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    print(client_socket.recv(BUFFER).decode("utf8"))
    command_choose = input("Choose command: ").encode("utf8")
    client_socket.send(command_choose)

