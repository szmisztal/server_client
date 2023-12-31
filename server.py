import socket as s
from datetime import datetime as dt
from communication_utils import CommunicationUtils
from data_utils import DataUtils, SQLite, PostgreSQL
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format, sqlite_database, postgreSQL_server_connection_dict
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
        self.sqlite_utils = SQLite(sqlite_database)
        # self.postgresql_utils = PostgreSQL(**postgreSQL_server_connection_dict)
        self.is_running = True
        self.server_start_date = "12.08.2023"
        self.server_version = "1.0.0"
        self.server_start_time = dt.now()

    def first_message_to_client(self):
        start_message = {
            "Client status": "CONNECTED",
            "Type 'help'": "to see available commands"
        }
        return start_message

    def read_client_request(self, client_request):
        deserialized_dict = self.data_utils.deserialize_json(client_request)
        print(deserialized_dict)
        if "Request" in deserialized_dict:
            request = deserialized_dict["Request"]
            return request
        else:
            user_data = deserialized_dict
            return user_data

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            client_ip = address[0]
            client_port = address[1]
            user = User("", "")
            print(f"Connection from {client_ip}:{client_port}")
            welcome_message = self.data_utils.serialize_to_json(self.first_message_to_client())
            client_socket.sendall(welcome_message)
            with client_socket:
                while self.is_running:
                    client_request_json = client_socket.recv(self.BUFFER)
                    client_request = self.read_client_request(client_request_json)
                    response_to_client = self.communication_utils.response_to_client(client_request, user)
                    response_to_client_json = self.data_utils.serialize_to_json(response_to_client)
                    if isinstance(response_to_client, dict):
                        if "Sign in successfully" in response_to_client.values():
                            user_data = client_request["Login"]
                            user = User(**user_data)
                            user.logged_in = True
                        elif "You was successfully log out" in response_to_client.values() or \
                                "You have been deleted from database" in response_to_client.values():
                            user = User("", "")
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

