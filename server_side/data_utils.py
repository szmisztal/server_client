import json
import bcrypt
# import psycopg2
import sqlite3
from sqlite3 import Error


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


class SQLite:
    def __init__(self, db_file):
        self.data_utils = DataUtils()
        self.db_file = db_file
        self.connection = self.create_connection()
        self.cursor = self.connection.cursor()
        self.create_user_table()
        self.create_message_table()

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.db_file)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def execute_sql_query(self, query, *args, fetch_option = None):
        with self.connection:
            try:
                self.cursor.execute(query, *args)
                self.connection.commit()
                if fetch_option == "fetchone":
                    return self.cursor.fetchone()
                elif fetch_option == "fetchall":
                    return self.cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
                self.connection.rollback()

    def create_user_table(self):
        create_user_table_query = """ CREATE TABLE IF NOT EXISTS users(
                                      user_id INTEGER PRIMARY KEY,
                                      username VARCHAR NOT NULL,
                                      password VARCHAR NOT NULL,
                                      sign_up_date DATE NOT NULL DEFAULT CURRENT_DATE,
                                      admin_role BOOLEAN NOT NULL DEFAULT FALSE
                                      ); """
        self.execute_sql_query(create_user_table_query)

    def create_message_table(self):
        create_message_table_query = """ CREATE TABLE IF NOT EXISTS messages(
                                         message_id INTEGER PRIMARY KEY,
                                         user_id INTEGER NOT NULL,
                                         sender VARCHAR NOT NULL,
                                         message_date DATE NOT NULL DEFAULT CURRENT_DATE,
                                         message_text VARCHAR(255) NOT NULL,
                                         archived BOOLEAN NOT NULL DEFAULT FALSE,
                                         FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                                         ); """
        self.execute_sql_query(create_message_table_query)

    def validate_username(self, username):
        query = "SELECT username FROM users WHERE username = ?"
        existing_username = self.execute_sql_query(query, (username, ), fetch_option = "fetchone")
        if existing_username is not None:
            return False
        return True

    def get_hashed_password_from_db(self, username):
        query = "SELECT password FROM users WHERE username = ?"
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
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        self.execute_sql_query(query, (username, hashed_password))

    def delete_user_from_db(self, username, password):
        query = "DELETE FROM users WHERE username = ? AND password = ?"
        self.execute_sql_query(query, (username, password))

    def update_user_data(self, new_username, new_password, username):
        new_hashed_password = self.data_utils.hash_password(new_password)
        query = "UPDATE users SET username = ?, password = ? WHERE username = ?"
        self.execute_sql_query(query, (new_username, new_hashed_password, username))

    def user_messages_list(self, username, boolean_condition):
        query = "SELECT sender, message_text FROM messages WHERE user_id = (SELECT user_id FROM users WHERE username = ?) " \
                "AND archived = ? ORDER BY message_date"
        messages_list = self.execute_sql_query(query, (username, boolean_condition), fetch_option = "fetchall")
        return messages_list

    def save_message_to_db(self, sender, message, recipient):
        get_recipient_query = "SELECT user_id FROM users WHERE username = ?"
        recipient_id = self.execute_sql_query(get_recipient_query, (recipient, ), fetch_option = "fetchone")
        message_save_query = "INSERT INTO messages (user_id, sender, message_text) VALUES (?, ?, ?)"
        self.execute_sql_query(message_save_query, (recipient_id[0], sender, message))

    def archive_messages(self, username):
        query = "UPDATE messages SET archived = True WHERE user_id = (SELECT user_id FROM users WHERE username = ?) AND archived = False"
        self.execute_sql_query(query, (username, ))


# class PostgreSQL:
#     def __init__(self, user, password, host, port, database):
#         self.user = user
#         self.password = password
#         self.host = host
#         self.port = port
#         self.database = database
#         self.data_utils = DataUtils()
#         self.create_user_table()
#         self.create_message_table()
#
#     def connection_to_db(self):
#         connection = psycopg2.connect(
#             user = self.user,
#             password = self.password,
#             host = self.host,
#             port = self.port,
#             database = self.database
#         )
#         return connection
#
#     def execute_sql_query(self, query, *args, fetch_option = None):
#         connection = self.connection_to_db()
#         try:
#             cursor = connection.cursor()
#             cursor.execute(query, *args)
#             connection.commit()
#             if fetch_option == "fetchone":
#                 return cursor.fetchone()
#             elif fetch_option == "fetchall":
#                 return cursor.fetchall()
#         except psycopg2.Error as e:
#             print(f"Error: {e}")
#             connection.rollback()
#         finally:
#             connection.close()
#
#     def check_that_table_exist(self, cursor, table_name):
#         table_exists_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
#         cursor.execute(table_exists_query)
#         table_exists = cursor.fetchone()[0]
#         if not table_exists:
#             return True
#         else:
#             return False
#
#     def create_user_table(self):
#         connection = self.connection_to_db()
#         try:
#             cursor = connection.cursor()
#             table_status = self.check_that_table_exist(cursor, "users")
#             if table_status == True:
#                 create_table_query = '''CREATE TABLE users(
#                                     user_id SERIAL PRIMARY KEY,
#                                     username VARCHAR NOT NULL,
#                                     password VARCHAR NOT NULL,
#                                     sign_up_date DATE NOT NULL DEFAULT CURRENT_DATE,
#                                     admin_role BOOLEAN NOT NULL DEFAULT FALSE
#                                     )'''
#                 cursor.execute(create_table_query)
#                 connection.commit()
#                 print("TABLE 'users' CREATED...")
#             else:
#                 print("TABLE 'users' EXISTS...")
#         except psycopg2.Error as e:
#             print(f"Error: {e}")
#         finally:
#             connection.close()
#
#     def create_message_table(self):
#         connection = self.connection_to_db()
#         try:
#             cursor = connection.cursor()
#             table_status = self.check_that_table_exist(cursor, "messages")
#             if table_status == True:
#                 create_table_query = '''CREATE TABLE messages(
#                                     message_id SERIAL PRIMARY KEY,
#                                     user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
#                                     sender VARCHAR NOT NULL,
#                                     message_date DATE NOT NULL DEFAULT CURRENT_DATE,
#                                     message_text VARCHAR(255) NOT NULL,
#                                     archived BOOLEAN NOT NULL DEFAULT FALSE
#                                     )'''
#                 cursor.execute(create_table_query)
#                 connection.commit()
#                 print("TABLE 'messages' CREATED")
#             else:
#                 print("TABLE 'messages' EXISTS")
#         except psycopg2.Error as e:
#             print(f"Error: {e}")
#         finally:
#             connection.close()
#
#     def validate_username(self, username):
#         validate_username_query = "SELECT username FROM users " \
#                                   "WHERE username = ?"
#         existing_username = self.execute_sql_query(validate_username_query, (username, ), fetch_option = "fetchone")
#         if existing_username is not None:
#             return False
#         else:
#             return True
#
#     def validate_credentials(self, username, password):
#         hashed_password_query = "SELECT password FROM users " \
#                                 "WHERE username = ?"
#         get_hashed_password = self.execute_sql_query(hashed_password_query, (username, ), fetch_option = "fetchone")
#         if get_hashed_password is not None:
#             hashed_password = get_hashed_password[0]
#             validate_password = self.data_utils.check_hashed_password(password, hashed_password)
#             if validate_password == True:
#                 validate_credentials_query = "SELECT username, password FROM users " \
#                                              "WHERE username = ? AND password = ?"
#                 credentials = self.execute_sql_query(validate_credentials_query, (username, hashed_password), fetch_option = "fetchone")
#                 if credentials is not None:
#                     return True
#                 else:
#                     return False
#             else:
#                 return False
#         else:
#             return False
#
#     def register_user_to_db(self, username, password):
#         insert_user_query = "INSERT INTO users (username, password) " \
#                             "VALUES (%s, %s)"
#         self.execute_sql_query(insert_user_query, (username, password))
#
#     def delete_user_from_db(self, username, password):
#         delete_user_query = "DELETE FROM users " \
#                             "WHERE username = %s AND password = %s"
#         self.execute_sql_query(delete_user_query, (username, password))
#
#     def update_user_data(self, new_username, new_password, username, password):
#         update_data_query = "UPDATE users " \
#                             "SET username = %s, password = %s " \
#                             "WHERE username = %s AND password = %s"
#         self.execute_sql_query(update_data_query, (new_username, new_password, username, password))
#
#     def user_messages_list(self, username, boolean_condition):
#         user_messages_list_query = "SELECT sender, message_text FROM messages " \
#                                    "WHERE user_id = (SELECT user_id FROM users WHERE username = ?) " \
#                                    "AND archived = ? " \
#                                    "ORDER BY message_date"
#         messages_list = self.execute_sql_query(user_messages_list_query, (username, boolean_condition), fetch_option = "fetchall")
#         return messages_list
#
#     def save_message_to_db(self, sender, message, recipient):
#             get_recipient_query = "SELECT user_id FROM users " \
#                                   "WHERE username = ?"
#             recipient_id = self.execute_sql_query(get_recipient_query, (recipient, ), fetch_option = "fetchone")
#             message_save_query = "INSERT INTO messages (user_id, sender, message_text) " \
#                                  "VALUES (?, ?, ?)"
#             self.execute_sql_query(message_save_query, (recipient_id[0], sender, message))
#
#     def archive_messages(self, username):
#         archive_messages_query = "UPDATE messages " \
#                                  "SET archived = True " \
#                                  "WHERE user_id = (SELECT user_id FROM users WHERE username = ?)" \
#                                  "AND archived = False"
#         self.execute_sql_query(archive_messages_query, (username, ))


