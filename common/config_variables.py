import os
import socket as s


server_HOST = "0.0.0.0"
client_HOST = "127.0.0.1"
PORT = 65432
BUFFER = 1024
encode_format = "UTF-8"
INTERNET_ADDRESS_FAMILY = s.AF_INET
SOCKET_TYPE = s.SOCK_STREAM


postgreSQL_database = "server_client"
postgreSQL_test_database = "server_client_test"
postgreSQL_server_connection_data = {
    "user": "postgres",
    "password": "postgres_password",
    "host": "db",
    "port": 5432,
    "database": postgreSQL_database
}

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")
log_file = os.path.join(LOG_DIR)

