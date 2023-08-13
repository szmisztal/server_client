import socket as s
import json
from variables import HOST, PORT, BUFFER, utf8, server_status

client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def deserialize_json(data):
    return json.loads(data)

def request_to_server():
    request = input("Choose command: uptime / info / help / stop \n").encode(utf8)
    return request

while server_status == True:
    client_socket.send(request_to_server())
    response = deserialize_json(client_socket.recv(BUFFER))
    for key, value in response.items():
        print(key, ":", value)
        if "Server status" in response.keys():
            server_status = False
            break

print("Client closed")



