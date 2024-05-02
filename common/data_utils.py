import json
import bcrypt
import psycopg2


class DataUtils:
    def __init__(self):
        self.encode_format = "UTF-8"

    def serialize_to_json(self, dict_data):
        return json.dumps(dict_data).encode(self.encode_format)

    def deserialize_json(self, dict_data):
        return json.loads(dict_data)

    def hash_password(self, raw_password):
        password = raw_password.encode(self.encode_format)
        salt = bcrypt.gensalt(rounds = 12)
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password

    def check_hashed_password(self, raw_password, hashed_password):
        password = raw_password.encode(self.encode_format)
        hashed_password = bytes.fromhex(hashed_password.replace("\\x", ""))
        validate_password = bcrypt.checkpw(password, hashed_password)
        return validate_password

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


class PostgreSQL:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.data_utils = DataUtils()
        self.initialize_db()

    def initialize_db(self):
        with self.connection_to_db() as conn:
            with conn.cursor() as cursor:
                self.create_user_table(cursor)
                self.create_message_table(cursor)

    def connection_to_db(self):
        try:
            connection = psycopg2.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port,
                database = self.database
            )
            return connection
        except psycopg2.Error as e:
            print(f"Failed to connect to the database: {e}")
            raise e

    def execute_sql_query(self, query, params = None, fetch_option = None):
        with self.connection_to_db() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, params)
                    conn.commit()
                    if fetch_option == "fetchone":
                        return cursor.fetchone()
                    elif fetch_option == "fetchall":
                        return cursor.fetchall()
                except psycopg2.Error as e:
                    conn.rollback()
                    print(f"An error occurred: {e}")
                    raise e

    def check_that_table_exist(self, table_name, cursor):
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
        cursor.execute(query)
        return cursor.fetchone()[0]

    def create_user_table(self, cursor):
        if not self.check_that_table_exist("users", cursor):
            query = """CREATE TABLE users(
                       user_id SERIAL PRIMARY KEY,
                       username VARCHAR NOT NULL,
                       password VARCHAR NOT NULL,
                       sign_up_date DATE NOT NULL DEFAULT CURRENT_DATE,
                       admin_role BOOLEAN NOT NULL DEFAULT FALSE
                       )"""
            cursor.execute(query)

    def create_message_table(self, cursor):
        if not self.check_that_table_exist("messages", cursor):
            query = """CREATE TABLE messages(
                       message_id SERIAL PRIMARY KEY,
                       user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                       sender VARCHAR NOT NULL,
                       message_date DATE NOT NULL DEFAULT CURRENT_DATE,
                       message_text VARCHAR(255) NOT NULL,
                       archived BOOLEAN NOT NULL DEFAULT FALSE
                       )"""
            cursor.execute(query)

    def validate_username(self, username):
        query = "SELECT username FROM users WHERE username = %s"
        existing_username = self.execute_sql_query(query, (username, ), fetch_option = "fetchone")
        if existing_username is not None:
            return True
        return False

    def get_hashed_password_from_db(self, username):
        query = "SELECT password FROM users WHERE username = %s"
        hashed_password = self.execute_sql_query(query, (username, ), fetch_option = "fetchone")
        return hashed_password[0]

    def validate_credentials(self, username, password):
        hashed_password = self.get_hashed_password_from_db(username)
        validate_password = self.data_utils.check_hashed_password(password, hashed_password)
        if validate_password:
            return True
        return False

    def register_user_to_db(self, username, raw_password):
        hashed_password = self.data_utils.hash_password(raw_password)
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.execute_sql_query(query, (username, hashed_password))

    def update_user_data(self, new_username, new_password, username):
        new_hashed_password = self.data_utils.hash_password(new_password)
        query = "UPDATE users SET username = %s, password = %s WHERE username = %s"
        self.execute_sql_query(query, (new_username, new_hashed_password, username))

    def delete_user_from_db(self, username):
        hashed_password = self.get_hashed_password_from_db(username)
        query = "DELETE FROM users WHERE username = %s AND password = %s"
        self.execute_sql_query(query, (username, hashed_password))

    def get_recipient_id(self, recipient_username):
        query = "SELECT user_id FROM users WHERE username = %s"
        return self.execute_sql_query(query, (recipient_username, ), fetch_option = "fetchone")

    def save_message_to_db(self, recipient, sender, message):
        recipient_id = self.get_recipient_id(recipient)
        message_save_query = "INSERT INTO messages (user_id, sender, message_text) VALUES (%s, %s, %s)"
        self.execute_sql_query(message_save_query, (recipient_id[0], sender, message))

    def user_messages_list(self, username, boolean_condition):
        query = "SELECT sender, message_text FROM messages WHERE user_id = (SELECT user_id FROM users WHERE username = %s) " \
                "AND archived = %s ORDER BY message_date"
        messages_list = self.execute_sql_query(query, (username, boolean_condition), fetch_option = "fetchall")
        return messages_list

    def archive_messages(self, username):
        query = "UPDATE messages SET archived = True WHERE user_id = (SELECT user_id FROM users WHERE username = %s) AND archived = False"
        self.execute_sql_query(query, (username, ))


