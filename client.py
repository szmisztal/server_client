from network_utils import client_socket_create
from communication_utils import request_to_server
from data_utils import serialize_json, deserialize_json
from variables import HOST, PORT, BUFFER, utf8
from models import User, user_username_and_password_input, recipient_input, message_input


client_socket = client_socket_create(HOST, PORT)
user = User("", "")

while True:
    request = request_to_server(user).encode(utf8)
    client_socket.send(request)
    if request.decode(utf8) == "stop":
        print("Client closed")
        client_socket.close()
        exit()
    elif request.decode(utf8) in ["register", "admin register", "login", "change data"]:
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
    elif request.decode(utf8) == "send message":
        recipient_data = recipient_input()
        recipient_json = serialize_json(recipient_data).encode(utf8)
        client_socket.send(recipient_json)
        response = deserialize_json(client_socket.recv(BUFFER))
        if "Error" in response:
            for key, value in response.items():
                print(f"{key}: {value}")
            continue
        for value in response.values():
            print(f"You`ll send message to: {value}")
        message = message_input()
        message_json = serialize_json(message).encode(utf8)
        client_socket.send(message_json)
        response_message = deserialize_json(client_socket.recv(BUFFER))
        for key, value in response_message.items():
            print(f"{key}: {value}")
    elif request.decode(utf8) in ["inbox", "archived messages"]:
        response = deserialize_json(client_socket.recv(BUFFER))
        for message in response:
            print(message)
    else:
        response = deserialize_json(client_socket.recv(BUFFER))
        for key, value in response.items():
            print(f"{key}: {value}")
