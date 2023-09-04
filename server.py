import socket as s
import json
from datetime import datetime as dt
from communication_utils import CommunicationUtils
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.communication_utils = CommunicationUtils(self)
        self.is_running = True
        self.server_start_date = "12.08.2023"
        self.server_version = "0.1.4"
        self.server_start_time = dt.now()

    def serialize_to_json(self, dict_data):
        return json.dumps(dict_data).encode(encode_format)

    def deserialize_json(self, dict_data):
        return json.loads(dict_data)

    def first_message_to_client(self):
        start_message = {
            "Welcome": "Type 'help' to see available commands"
        }
        return start_message

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            client_ip = address[0]
            client_port = address[1]
            print(f"Connection from {client_ip}:{client_port}")
            client_socket.sendall(self.first_message_to_client())
            with client_socket:
                while self.is_running:
                    client_request = client_socket.recv(self.BUFFER)
                    response_to_client = self.response_to_client(client_request)
                    response_to_client_json = serialize_to_json(response_to_client)
                    client_socket.sendall(response_to_client_json)


if __name__ == "__main__":
    server = Server()
    print("THE SERVER STARTS...")
    server.start()

