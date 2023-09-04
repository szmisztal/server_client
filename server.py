import socket as s
from communication_utils import Request, Response
from data_utils import serialize_to_json, deserialize_json
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.request_from_client = Request()
        self.response_to_client = Response()
        self.is_running = True
        self.server_start_date = "12.08.2023"
        self.server_version = "0.1.4"

    def first_message_to_client(self, client_ip, client_port):
        start_message = {
            "Message": f"Welcome {client_ip}:{client_port}",
            "Commands": "Type 'help' to see available commands"
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
            first_message_json = serialize_to_json(self.first_message_to_client(client_ip, client_port))
            client_socket.sendall(first_message_json)

            with client_socket:
                while self.is_running:
                    client_request = client_socket.recv(self.BUFFER)
                    deserialize_json(client_request)
                    print(client_request)


if __name__ == "__main__":
    server = Server()
    print("The server starts")
    server.start()

