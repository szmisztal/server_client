import socket as s
from data_utils import DataUtils
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format


class Client:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.data_utils = DataUtils()
        self.is_running = True

    def make_request_to_server(self):
        client_input = input()
        if client_input == "register":
            user_data = self.user_data_input()
            return user_data
        else:
            request_to_server = {
                "Request": client_input
            }
            return request_to_server

    def read_server_response(self, dict_data):
        deserialized_dict = self.data_utils.deserialize_json(dict_data)
        for key, value in deserialized_dict.items():
            print(f"{key}: {value}")

    def user_data_input(self):
        username = input("Username: ")
        password = input("Password: ")
        user_data = {
            "username": username,
            "password": password
        }
        user_data_request = {
            "Register": user_data
        }
        return user_data_request

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            client_socket.connect((HOST, PORT))
            server_response = client_socket.recv(self.BUFFER)
            self.read_server_response(server_response)
            while self.is_running:
                client_request = self.make_request_to_server()
                client_request_json = self.data_utils.serialize_to_json(client_request)
                client_socket.sendall(client_request_json)
                server_response = client_socket.recv(self.BUFFER)
                self.read_server_response(server_response)
                self.stop(server_response)

    def stop(self, dict_data):
        deserialized_dict = self.data_utils.deserialize_json(dict_data)
        if "Server status" in deserialized_dict and "Shutting down" in deserialized_dict["Server status"]:
            print("CLIENT CLOSED...")
            self.is_running = False
        else:
            pass


if __name__ == "__main__":
    client = Client()
    client.start()
