import socket
from data_utils import serialize_to_json, deserialize_json
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER


class Client:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.is_running = True

    def start(self):
        with socket.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            client_socket.connect((HOST, PORT))
            server_response = client_socket.recv(self.BUFFER)
            deserialize_json(server_response)
            print(server_response)
            client_input = input()
            client_request = {"Command": client_input}
            serialize_to_json(client_request)
            client_socket.sendall(client_request)


if __name__ == "__main__":
    client = Client()
    client.start()
