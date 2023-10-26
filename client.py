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

    def make_request_to_server(self, client_input):
        if client_input in ["register", "login", "change data"]:
            user_data_input = self.user_data_input()
            if client_input == "register":
                user_data = {
                    "Register": user_data_input
                }
                return user_data
            elif client_input == "login":
                user_data = {
                    "Login": user_data_input
                }
                return user_data
            elif client_input == "change data":
                user_data = {
                    "New data": user_data_input
                }
                return user_data
        elif client_input == "send message":
            message_data = self.send_message_input()
            return message_data
        elif client_input == "delete":
            delete_input = self.delete_user_input()
            return delete_input
        else:
            request_to_server ={
                "Request": client_input
            }
            return request_to_server

    def user_data_input(self):
        username = input("Username: ")
        password = input("Password: ")
        user_data = {
            "username": username,
            "password": password
        }
        return user_data

    def send_message_input(self):
        recipient = input("Who do you want to send a message to ?: ")
        message = input("Write a message: ")
        message_data = {
            "Recipient": recipient,
            "Message": message
        }
        return message_data

    def delete_user_input(self):
        confirmation = input("Do you really want to delete your data from database ? YES/NO: ").lower()
        confirmation_data = {
            "Delete confirmation": confirmation
        }
        return confirmation_data

    def read_server_response(self, dict_data):
        deserialized_data = self.data_utils.deserialize_json(dict_data)
        if isinstance(deserialized_data, dict):
            for key, value in deserialized_data.items():
                print(f">>> {key}: {value}")
        elif isinstance(deserialized_data, list):
            if deserialized_data == []:
                print("You don`t have any messages to read")
            else:
                for message in deserialized_data:
                    sender = message[0]
                    message_text = message[1]
                    print(f"Message from: {sender} \nText: {message_text} \n"
                          "--------------------------------------------------------")

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            client_socket.connect((HOST, PORT))
            server_response = client_socket.recv(self.BUFFER)
            self.read_server_response(server_response)
            while self.is_running:
                client_input = input("REQUEST: ").lower()
                client_request = self.make_request_to_server(client_input)
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


if __name__ == "__main__":
    client = Client()
    client.start()
