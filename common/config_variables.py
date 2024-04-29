import socket as s
import os


server_HOST = "0.0.0.0"
client_HOST = "sc-server"
PORT = 65432
BUFFER = 1024
encode_format = "UTF-8"
INTERNET_ADDRESS_FAMILY = s.AF_INET
SOCKET_TYPE = s.SOCK_STREAM

sqlite_db_base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sqlite_database_path = os.path.join(sqlite_db_base_directory, "../sqlite_server-client_db.db")
sqlite_test_database = "sqlite_server-client_test_db.db"

postgreSQL_database = "postgreSQL_server_client_db"
postgreSQL_test_database = "postgreSQL_server_client_test_db"
postgreSQL_server_connection_dict = {
    "user": "postgres",
    "password": "postgres-password",
    "host": server_HOST,
    "port": PORT,
    "database": postgreSQL_database
}



