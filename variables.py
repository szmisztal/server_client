import socket as s
from secrets import password


HOST = "127.0.0.1"
PORT = 65432
BUFFER = 1024
encode_format = "UTF-8"
INTERNET_ADDRESS_FAMILY = s.AF_INET
SOCKET_TYPE = s.SOCK_STREAM
sqlite_database = "sqlite_server-client_db.db"
sqlite_test_database = "sqlite_server-client_test_db.db"
postgreSQL_database = "postgreSQL_server_client_db"
postgreSQL_test_database = "postgreSQL_server_client_test_db"
postgreSQL_server_connection_dict = {
    "user": "postgres",
    "password": password,
    "host": HOST,
    "port": PORT,
    "database": postgreSQL_database
}


