import socket as s
import os
import logging


HOST = "127.0.0.1"
PORT = 65432
BUFFER = 1024
encode_format = "UTF-8"
INTERNET_ADDRESS_FAMILY = s.AF_INET
SOCKET_TYPE = s.SOCK_STREAM

sqlite_db_base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sqlite_database_path = os.path.join(sqlite_db_base_directory, "sqlite_server-client_db.db")
sqlite_test_database = "sqlite_server-client_test_db.db"

postgreSQL_database = "postgreSQL_server_client_db"
postgreSQL_test_database = "postgreSQL_server_client_test_db"
postgreSQL_server_connection_dict = {
    "user": "postgres",
    "password": "postgres-password",
    "host": HOST,
    "port": PORT,
    "database": postgreSQL_database
}


def logger_config(logger_name, log_folder, log_file_name):
    log_path = os.path.join(logger_name, log_folder, log_file_name)
    logging.basicConfig(
        level = logging.DEBUG,
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(logger_name)
