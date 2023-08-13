import socket as s
import json
from datetime import datetime as dt
from variables import HOST, PORT, BUFFER, utf8, server_version, server_start_date, server_status, server_uptime

def serialize_json(data):
    return json.dumps(data).encode(utf8)

def uptime(server_start_time):
    current_time = dt.now()
    server_uptime = current_time - server_start_time
    uptime_dict = {
        "Server uptime time:": f"{server_uptime}"
    }
    return serialize_json(uptime_dict)

def info():
    server_info = {
        "Server start date:": server_start_date,
        "Server version:": server_version
    }
    return serialize_json(server_info)

def help():
    commands = {
        "Uptime": "Shows the lifetime of the server",
        "Info": "Shows the current version and server start date",
        "Help": "Shows available commands",
        "Stop": "Shuts down the server"
    }
    return serialize_json(commands)

def stop():
    stop_msg = {
        "Server status": "Shutting down"
    }
    return serialize_json(stop_msg)

def response_to_client(client_request):
    if client_request == "uptime":
        return uptime(server_uptime)
    elif client_request == "info":
        return info()
    elif client_request == "help":
        return help()
    else:
        error_msg = {
            "Unknown command": f"'{client_request}', try again"
        }
        return serialize_json(error_msg)

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
client_socket, address = server_socket.accept()

while server_status == True:
    client_request = client_socket.recv(BUFFER).decode(utf8)
    print(f"Client request: {client_request}")
    if client_request == "stop":
        client_socket.send(stop())
        server_status = False
        break
    else:
        response_data = response_to_client(client_request)
        client_socket.send(response_data)

print("Server closed")
