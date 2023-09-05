import socket as s
import json
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format


class Client:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.is_running = True

    def serialize_to_json(self, dict_data):
        return json.dumps(dict_data).encode(encode_format)

    def deserialize_json(self, dict_data):
        return json.loads(dict_data)

    def make_request_to_server(self, client_input):
        request_to_server = {
            "Request": client_input
        }
        return request_to_server

    def read_response_dict(self, dict_data):
        deserialized_dict = self.deserialize_json(dict_data)
        for key, value in deserialized_dict.items():
            print(f"{key}: {value}")

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            client_socket.connect((HOST, PORT))
            server_response = client_socket.recv(self.BUFFER)
            self.read_response_dict(server_response)
            while self.is_running:
                client_input = input()
                client_request = self.make_request_to_server(client_input)
                client_request_json = self.serialize_to_json(client_request)
                client_socket.sendall(client_request_json)
                server_response = client_socket.recv(self.BUFFER)
                self.read_response_dict(server_response)
                self.stop(server_response)

    def stop(self, dict_data):
        deserialized_dict = self.deserialize_json(dict_data)
        if "Server status" in deserialized_dict and "Shutting down" in deserialized_dict["Server status"]:
            print("CLIENT CLOSED...")
            self.is_running = False
        else:
            pass


if __name__ == "__main__":
    client = Client()
    client.start()
