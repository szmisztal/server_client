import socket as s


HOST = "127.0.0.1"
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
    "host": HOST,
    "port": 5432,
    "database": postgreSQL_database
}



