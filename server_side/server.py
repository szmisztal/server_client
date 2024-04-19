import sys
sys.path.clear()
sys.path.extend([
    'C:\\Programy\\Python\\Projekty\\server_client\\client_side',
    'C:\\Programy\\Python\\Projekty\\server_client\\server_side',
    'C:\\Program Files\\Python38\\python38.zip',
    'C:\\Program Files\\Python38\\DLLs',
    'C:\\Program Files\\Python38\\lib',
    'C:\\Program Files\\Python38',
    'C:\\Users\\szmis\\AppData\\Roaming\\Python\\Python38\\site-packages',
    'C:\\Program Files\\Python38\\lib\\site-packages',
    'C:\\Programy\\Python\\Projekty\\server_client'
])
import socket as s
from datetime import datetime as dt
from server_messages import HandlingClientCommands
from data_utils import DataUtils
from config_variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.responses = HandlingClientCommands(self)
        self.data_utils = DataUtils()
        self.is_running = True
        self.server_start_date = "12.08.2023"
        self.server_version = "1.3.3"
        self.server_start_time = dt.now()

    def connect_with_client(self, server_socket):
        server_socket.bind((self.HOST, self.PORT))
        server_socket.listen()
        client_socket, address = server_socket.accept()
        print(f"Connection from {address[0]}:{address[1]}")
        self.initial_correspondence_with_client(client_socket)
        return client_socket

    def initial_correspondence_with_client(self, client_socket):
        welcome_message = self.data_utils.serialize_to_json(self.responses.response.welcome_message())
        client_socket.sendall(welcome_message)

    def read_client_request(self, client_socket):
        client_request_json = client_socket.recv(self.BUFFER)
        client_request = self.data_utils.deserialize_json(client_request_json)
        for key, value in client_request.items():
            print(f">>> {key}: {value}")
        return client_request["message"], client_request["data"]

    def send_response_to_client(self, server_socket, client_request, client_socket):
        response_to_client = self.responses.response_to_client(client_request)
        response_to_client_json = self.data_utils.serialize_to_json(response_to_client)
        if response_to_client["message"] == "Server`s shutting down...":
            self.stop(server_socket, client_socket, response_to_client_json)
        client_socket.sendall(response_to_client_json)

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            client_socket = self.connect_with_client(server_socket)
            with client_socket:
                while self.is_running:
                    client_request = self.read_client_request(client_socket)
                    self.send_response_to_client(server_socket, client_request, client_socket)

    def stop(self, server_socket, client_socket, closing_message):
        client_socket.sendall(closing_message)
        print("SERVER CLOSED...")
        self.is_running = False
        client_socket.close()
        server_socket.close()



if __name__ == "__main__":
    server = Server()
    print("SERVER`S UP...")
    server.start()

