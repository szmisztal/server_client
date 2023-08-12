import socket as s
import json
from datetime import datetime as dt
from variables import HOST, PORT, BUFFER, utf8, server_version, server_start_date, server_uptime

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

def serialize_json(data):
    serializing_data = json.dumps(data)
    return serializing_data

def uptime(server_uptime):
    current_time = dt.now()
    server_uptime = current_time - server_uptime
    return serialize_json(server_uptime).encode(utf8)

def info():
    server_info = (f"Server start date: {server_start_date}, server version: {server_version}")
    return serialize_json(server_info).encode(utf8)

def help():
    commands = {
        "Uptime": "Shows the lifetime of the server",
        "Info": "Shows the current version and server start date",
        "Help": "Shows available commands",
        "Stop": "Shuts down the server"
        }
    return serialize_json(commands).encode(utf8)

def stop():
    pass

def receive_request_from_client():
    client_request = client_socket.recv(BUFFER).decode(utf8)
    return client_request

def response_to_client():
    if receive_request_from_client() == "uptime":
        client_socket.send(uptime(server_uptime))
    elif receive_request_from_client() == "info":
        client_socket.send(info())
    elif receive_request_from_client() == "help":
        client_socket.send(help())
    elif receive_request_from_client() == "stop":
        stop()

while True:
    sever_start = dt.now()
    client_socket, address = server_socket.accept()
    print(f"Connection from {HOST}:{PORT}")
    print(receive_request_from_client())
    print(response_to_client())
