from network_utils import client_socket_create
from communication_utils import request_to_server
from data_utils import serialize_json, deserialize_json, user_username_and_password_input
from variables import HOST, PORT, BUFFER, utf8
from models import User


client_socket = client_socket_create(HOST, PORT)
user = User("", "")

while True:
    request = request_to_server(user).encode(utf8)
    client_socket.send(request)
    if request.decode(utf8) == "stop":
        print("Client closed")
        client_socket.close()
        exit()
    elif request.decode(utf8) in ["register", "login", "change data"]:
        user_data = user_username_and_password_input()
        user_json_data = serialize_json(user_data).encode(utf8)
        client_socket.send(user_json_data)
        response = deserialize_json(client_socket.recv(BUFFER))
        for key, value in response.items():
            print(f"{key} : {value}")
        if "Message" in response and "logged in" in response["Message"]:
            user = User(**user_data)
            user.logged_in = True
    elif request.decode(utf8) == "logout":
        if user.logged_in == True:
            user.logged_in = False
            response = deserialize_json(client_socket.recv(BUFFER))
            for key, value in response.items():
                print(f"{key}: {value}")
    else:
        response = deserialize_json(client_socket.recv(BUFFER))
        for key, value in response.items():
            print(f"{key}: {value}")







