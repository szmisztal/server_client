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
from server_side.data_utils import DataUtils
from client_messages import ClientRequests
from config_variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format


class Client:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.data_utils = DataUtils()
        self.client_requests = ClientRequests()
        self.is_running = True

    def send_command(self, client_socket):
        client_request = self.client_requests.request_to_server()
        client_request_json = self.data_utils.serialize_to_json(client_request)
        client_socket.sendall(client_request_json)

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

    def read_server_response(self, client_socket):
        server_response = client_socket.recv(self.BUFFER)
        deserialized_response = self.data_utils.deserialize_json(server_response)
        for key, value in deserialized_response.items():
            print(f">>> {key}: {value}")
        if "Server`s shutting down..." in deserialized_response["message"]:
            self.stop()
        # elif isinstance(deserialized_data, list):
        #     if not deserialized_data:
        #         print("You don`t have any messages to read")
        #     else:
        #         for message in deserialized_data:
        #             print(f"Message from: {message[0]} \nText: {message[1]} \n"
        #                   f"--------------------------------------------------------")

    def start(self):
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as client_socket:
            client_socket.connect((self.HOST, self.PORT))
            self.read_server_response(client_socket)
            while self.is_running:
                self.send_command(client_socket)
                self.read_server_response(client_socket)

    def stop(self):
        print("CLIENT CLOSED...")
        self.is_running = False



if __name__ == "__main__":
    client = Client()
    client.start()
