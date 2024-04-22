import logging
import os
import socket as s
from server_side.data_utils import DataUtils
from client_messages import ClientRequests
from config_variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format, logger_config


class Client:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.logger = logger_config("Client", os.getcwd(), "client_logs.log")
        self.data_utils = DataUtils()
        self.client_requests = ClientRequests()
        self.is_running = True

    def send_command(self, client_socket):
        try:
            client_request = self.client_requests.request_to_server()
            client_request_json = self.data_utils.serialize_to_json(client_request)
            client_socket.sendall(client_request_json)
        except OSError as e:
            self.logger.debug(f"Error: {e}")
            self.stop(client_socket)


    def read_server_response(self, client_socket):
        try:
            server_response = client_socket.recv(self.BUFFER)
            deserialized_response = self.data_utils.deserialize_json(server_response)
            for key, value in deserialized_response.items():
                print(f">>> {key}: {value}")
            if "Server`s shutting down..." in deserialized_response["message"]:
                self.stop(client_socket)
        except OSError as e:
            self.logger.debug(f"Error: {e}")
            self.stop(client_socket)

    def main(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as client_socket:
            client_socket.connect((self.HOST, self.PORT))
            self.read_server_response(client_socket)
            while self.is_running:
                self.send_command(client_socket)
                self.read_server_response(client_socket)

    def stop(self, client_socket):
        self.logger.debug("CLIENT CLOSED...")
        self.is_running = False
        client_socket.close()



if __name__ == "__main__":
    client = Client()
    logging.debug("CLIENT`S UP")
    client.main()
