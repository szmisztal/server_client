import json
import psycopg2
from variables import encode_format
from secrets import password

class DataUtils:
    def serialize_to_json(self, dict_data):
        return json.dumps(dict_data).encode(encode_format)

    def deserialize_json(self, dict_data):
        return json.loads(dict_data)

    def create_table(self, name):
        self.connection = psycopg2.connect(
            user = "postgres",
            password = password,
            host = "127.0.0.1",
            port = "5432",
            database = "postgres_db"
        )
        cursor = self.connection.cursor()
        create_table_query = f'''CREATE TABLE {name}
                        (ID SERIAL PRIMARY KEY,
                        USERNAME VARCHAR NOT NULL,
                        PASSWORD VARCHAR NOT NULL,
                        ADMIN_ROLE BOOLEAN NOT NULL DEFAULT FALSE)'''
        cursor.execute(create_table_query)
        self.connection.commit()
        print("Table was created")

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
