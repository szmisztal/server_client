import logging
import socket as s
from datetime import datetime as dt
from server_messages import HandlingClientCommands
from common.serialize_utils import SerializeUtils
from common.config_variables import server_HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format, log_file
from common.logger_config import logger_config


class Server:
    """
    A class representing a server that communicates with clients.

    Attributes:
    ----------
    HOST : str
        The IP address on which the server listens.
    PORT : int
        The port on which the server listens.
    INTERNET_ADDRESS_FAMILY : int
        The address family (e.g., AF_INET).
    SOCKET_TYPE : int
        The socket type (e.g., SOCK_STREAM).
    BUFFER : int
        The buffer size for receiving data.
    encode_format : str
        The format used for encoding messages.
    logger : logging.Logger
        The logger for server messages.
    responses : HandlingClientCommands
        The handler for client commands.
    serialize_utils : SerializeUtils
        Utility for serializing and deserializing data.
    is_running : bool
        Flag indicating if the server is running.
    server_start_date : str
        The start date of the server.
    server_version : str
        The version of the server.
    server_start_time : datetime
        The start time of the server.
    """

    def __init__(self):
        """
        Initializes the server with specified configurations.
        """
        self.HOST = server_HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.logger = logger_config("Server", log_file, "server_logs.log")
        self.responses = HandlingClientCommands(self)
        self.serialize_utils = SerializeUtils()
        self.is_running = True
        self.server_start_date = "12.08.2023"
        self.server_version = "1.7.0"
        self.server_start_time = dt.now()

    def connect_with_client(self, server_socket):
        """
        Connects with a client.

        Parameters:
        ----------
        server_socket : socket.socket
            The server socket used for accepting connections.

        Returns:
        -------
        socket.socket
            The client socket if the connection is successful, None otherwise.

        Logs errors if the connection fails.
        """
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
        """
        Sends the initial welcome message to the client.

        Parameters:
        ----------
        client_socket : socket.socket
            The client socket to communicate with.
        """
        welcome_message = self.serialize_utils.serialize_to_json(self.responses.response.welcome_message())
        client_socket.sendall(welcome_message)

    def read_client_request(self, client_socket):
        """
        Reads the client's request.

        Parameters:
        ----------
        client_socket : socket.socket
            The client socket to read the request from.

        Returns:
        -------
        tuple
            The message and data from the client's request.
        """
        client_request_json = client_socket.recv(self.BUFFER)
        client_request = self.serialize_utils.deserialize_json(client_request_json)
        for key, value in client_request.items():
            print(f">>> {key}: {value}")
        return client_request["message"], client_request["data"]

    def send_response_to_client(self, server_socket, client_request, client_socket):
        """
        Sends a response to the client based on their request.

        Parameters:
        ----------
        server_socket : socket.socket
            The server socket used for communication.
        client_request : dict
            The client's request.
        client_socket : socket.socket
            The client socket to send the response to.

        Logs errors if sending the response fails.
        """
        try:
            response_to_client = self.responses.response_to_client(client_request)
            response_to_client_json = self.serialize_utils.serialize_to_json(response_to_client)
            if response_to_client["message"] == "Server`s shutting down...":
                self.stop(server_socket, client_socket, response_to_client_json)
            client_socket.sendall(response_to_client_json)
        except OSError as e:
            client_socket.close()
            self.logger.debug(f"Error: {e}")

    def main(self):
        """
        The main method to run the server.

        Creates the server socket, accepts client connections,
        and handles client requests and responses.
        """
        with s.socket(self.INTERNET_ADDRESS_FAMILY, self.SOCKET_TYPE) as server_socket:
            client_socket = self.connect_with_client(server_socket)
            with client_socket:
                while self.is_running:
                    client_request = self.read_client_request(client_socket)
                    self.send_response_to_client(server_socket, client_request, client_socket)

    def stop(self, server_socket, client_socket, closing_message):
        """
        Stops the server and closes the connection with the client.

        Parameters:
        ----------
        server_socket : socket.socket
            The server socket to close.
        client_socket : socket.socket
            The client socket to close.
        closing_message : bytes
            The closing message to send to the client.
        """
        client_socket.sendall(closing_message)
        self.logger.debug("SERVER CLOSED...")
        self.is_running = False
        server_socket.close()


if __name__ == "__main__":
    server = Server()
    logging.debug("SERVER`S UP...")
    server.main()


