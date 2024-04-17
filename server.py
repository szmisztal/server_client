import socket as s
from datetime import datetime as dt
from communication_utils import ServerResponses
from data_utils import DataUtils, SQLite
from config_variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format, sqlite_database, postgreSQL_server_connection_dict
from users_utils import User


class Server:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.server_responses = ServerResponses(self)
        self.data_utils = DataUtils()
        self.sqlite_utils = SQLite(sqlite_database)
        # self.postgresql_utils = PostgreSQL(**postgreSQL_server_connection_dict)
        self.is_running = True
        self.server_start_date = "12.08.2023"
        self.server_version = "1.2.0"
        self.server_start_time = dt.now()

    def read_client_request(self, client_socket):
        client_request_json = client_socket.recv(self.BUFFER)
        client_request = self.data_utils.deserialize_json(client_request_json)
        for key, value in client_request.items():
            print(f">>> {key}: {value}")
        request = client_request["message"]
        return request

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            print(f"Connection from {address[0]}:{address[1]}")
            welcome_message = self.data_utils.serialize_to_json(self.server_responses.welcome_message())
            client_socket.sendall(welcome_message)
            with client_socket:
                while self.is_running:
                    client_request = self.read_client_request(client_socket)
                    response_to_client = self.server_responses.response_to_client(client_request)
                    response_to_client_json = self.data_utils.serialize_to_json(response_to_client)
                    # if isinstance(response_to_client, dict):
                    #     if "Sign in successfully" in response_to_client.values():
                    #         user_data = client_request["Login"]
                    #         user = User(**user_data)
                    #         user.logged_in = True
                    #     elif "You was successfully log out" in response_to_client.values() or \
                    #             "You have been deleted from database" in response_to_client.values():
                    #         user = User("", "")
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

