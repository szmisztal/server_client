import socket as s
from data_utils import DataUtils
from communication_utils import ClientRequests
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
        client_request = self.client_requests.command_input()
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
        deserialized_data = self.data_utils.deserialize_json(server_response)
        if isinstance(deserialized_data, dict):
            for key, value in deserialized_data.items():
                print(f">>> {key}: {value}")
        elif isinstance(deserialized_data, list):
            if not deserialized_data:
                print("You don`t have any messages to read")
            else:
                for message in deserialized_data:
                    print(f"Message from: {message[0]} \nText: {message[1]} \n"
                          f"--------------------------------------------------------")

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            client_socket.connect((HOST, PORT))
            self.read_server_response(client_socket)
            while self.is_running:
                self.send_command(client_socket)
                self.read_server_response(client_socket)

if __name__ == "__main__":
    client = Client()
    client.start()
