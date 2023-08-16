from network_utils import client_socket_create
from communication_utils import request_to_server
from data_utils import deserialize_json
from variables import HOST, PORT, BUFFER, utf8

client_socket = client_socket_create(HOST, PORT)


while True:
    request = request_to_server()
    client_socket.send(request)
    if request.decode(utf8) == "stop":
        print("Client closed")
        client_socket.close()
        exit()
    else:
        response = deserialize_json(client_socket.recv(BUFFER))
        for key, value in response.items():
            print(f"{key} : {value}")





