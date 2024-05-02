import logging
import os
import socket as s
from datetime import datetime as dt
from server_messages import HandlingClientCommands
from common.data_utils import DataUtils
from common.config_variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from common.logger_config import logger_config


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.logger = logger_config("Server", os.getcwd(), "server_logs.log")
        self.responses = HandlingClientCommands(self)
        self.data_utils = DataUtils()
        self.is_running = True
        self.server_start_date = "12.08.2023"
        self.server_version = "1.5.2"
        self.server_start_time = dt.now()

    def connect_with_client(self, server_socket):
        client_socket = None
        try:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            self.logger.debug(f"Connection from {address[0]}:{address[1]}")
            self.initial_correspondence_with_client(client_socket)
            return client_socket
        except OSError as e:
            if client_socket:
                client_socket.close()
            self.logger.error(f"Error connecting to client: {e}")

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
        try:
            response_to_client = self.responses.response_to_client(client_request)
            response_to_client_json = self.data_utils.serialize_to_json(response_to_client)
            if response_to_client["message"] == "Server`s shutting down...":
                self.stop(server_socket, client_socket, response_to_client_json)
            client_socket.sendall(response_to_client_json)
        except OSError as e:
            client_socket.close()
            self.logger.debug(f"Error: {e}")

    def main(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            client_socket = self.connect_with_client(server_socket)
            with client_socket:
                while self.is_running:
                    client_request = self.read_client_request(client_socket)
                    self.send_response_to_client(server_socket, client_request, client_socket)

    def stop(self, server_socket, client_socket, closing_message):
        client_socket.sendall(closing_message)
        self.logger.debug("SERVER CLOSED...")
        self.is_running = False
        server_socket.close()



if __name__ == "__main__":
    server = Server()
    logging.debug("SERVER`S UP...")
    server.main()

