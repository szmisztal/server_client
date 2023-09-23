import json
import psycopg2
from variables import encode_format
from secrets import password

class DataUtils:
    def serialize_to_json(self, dict_data):
        return json.dumps(dict_data).encode(encode_format)

    def deserialize_json(self, dict_data):
        return json.loads(dict_data)

    def connection_to_db(self):
        connection = psycopg2.connect(
            user = "postgres",
            password = password,
            host = "127.0.0.1",
            port = "5432",
            database = "server_client_db"
        )
        return connection

    def check_that_table_exist(self, cursor, table_name):
        table_exists_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
        cursor.execute(table_exists_query)
        table_exists = cursor.fetchone()[0]
        if not table_exists:
            return True
        else:
            return False

    def create_user_table(self):
        connection = self.connection_to_db()
        cursor = connection.cursor()
        table_status = self.check_that_table_exist(cursor, "users")
        if table_status == True:
            create_table_query = '''CREATE TABLE users(
                                user_id SERIAL PRIMARY KEY,
                                username VARCHAR NOT NULL,
                                password VARCHAR NOT NULL,
                                admin_role BOOLEAN NOT NULL DEFAULT FALSE
                                )'''
            cursor.execute(create_table_query)
            connection.commit()
            print("TABLE 'users' CREATED...")
        else:
            print("TABLE 'users' EXISTS...")

    def create_message_table(self):
        connection = self.connection_to_db()
        cursor = connection.cursor()
        table_status = self.check_that_table_exist(cursor, "messages")
        if table_status == True:
            create_table_query = '''CREATE TABLE messages(
                                message_id SERIAL PRIMARY KEY,
                                user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                                sender VARCHAR NOT NULL,
                                text VARCHAR(255) NOT NULL,
                                archived BOOLEAN NOT NULL DEFAULT FALSE
                                )'''
            cursor.execute(create_table_query)
            connection.commit()
            print("TABLE 'messages' CREATED")
        else:
            print("TABLE 'messages' EXISTS")

    def write_to_json_file(self, filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent = 4)

    def read_json_file(self, filename):
        try:
            with open(filename, "r") as file:
                users_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users_data = []
        return users_data
