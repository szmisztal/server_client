import socket as s
from datetime import datetime as dt
from communication_utils import CommunicationUtils
from data_utils import DataUtils
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from users_utils import User


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.communication_utils = CommunicationUtils(self)
        self.data_utils = DataUtils()
        self.is_running = True
        self.server_start_date = "12.08.2023"
        self.server_version = "0.2.6"
        self.server_start_time = dt.now()

    def first_message_to_client(self):
        start_message = {
            "Welcome": "Type 'help' to see available commands"
        }
        return start_message

    def read_client_request(self, client_request):
        deserialized_dict = self.data_utils.deserialize_json(client_request)
        print(deserialized_dict)
        request = deserialized_dict.get("Request").lower()
        return request

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            client_ip = address[0]
            client_port = address[1]
            print(f"Connection from {client_ip}:{client_port}")
            welcome_message = self.data_utils.serialize_to_json(self.first_message_to_client())
            client_socket.sendall(welcome_message)
            with client_socket:
                while self.is_running:
                    client_request_json = client_socket.recv(self.BUFFER)
                    client_request = self.read_client_request(client_request_json)
                    response_to_client = self.communication_utils.response_to_client(client_request)
                    response_to_client_json = self.data_utils.serialize_to_json(response_to_client)
                    client_socket.sendall(response_to_client_json)

    def stop(self):
        stop_message = {
            "Server status": "Shutting down"
        }
        print("SERVER CLOSED...")
        self.is_running = False
        return stop_message


if __name__ == "__main__":
    server = Server()
    print("SERVER`S UP...")
    server.start()

