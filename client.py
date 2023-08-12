import socket as s
import json
from variables import HOST, PORT, BUFFER, utf8

client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def deserialize_json(data):
    deserialized_data = json.loads(data)
    return deserialized_data

def receive_request_from_server():
    server_request = client_socket.recv(BUFFER).decode(utf8)
    return deserialize_json(server_request)

def response_to_server():
    response = input("Choose command: uptime / info / help / stop \n").encode(utf8)
    return client_socket.send(response)

while True:
    print(response_to_server())
    print(receive_request_from_server())



