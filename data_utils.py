import json
import sqlite3
from sqlite3 import Error
from variables import encode_format, db_file_name


class DataUtils:
    def serialize_to_json(self, dict_data):
        return json.dumps(dict_data).encode(encode_format)

    def deserialize_json(self, dict_data):
        return json.loads(dict_data)

    def create_connection(self, db_file):
        try:
            connection = sqlite3.connect(db_file)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def execute_sql_query(self, query, *args, fetch_option = None):
        connection = self.create_connection(db_file_name)
        cursor = connection.cursor()
        if connection is not None:
            try:
                cursor.execute(query, *args)
                connection.commit()
                if fetch_option == "fetchone":
                    return cursor.fetchone()
                elif fetch_option == "fetchall":
                    return cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        else:
            print("Cannot create the database connection.")

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
        validate_username_query = "SELECT username FROM users " \
                                  "WHERE username = ?"
        existing_username = self.execute_sql_query(validate_username_query, (username, ), fetch_option = "fetchone")
        if existing_username is not None:
            return False
        else:
            return True

    def validate_credentials(self, username, password):
        validate_credentials_query = "SELECT username, password FROM users " \
                                     "WHERE username = ? AND password = ?"
        credentials = self.execute_sql_query(validate_credentials_query, (username, password), fetch_option = "fetchone")
        if credentials is not None:
            return True
        else:
            return False

    def register_user_to_db(self, username, password):
        insert_user_query = "INSERT INTO users (username, password) " \
                            "VALUES (?, ?)"
        self.execute_sql_query(insert_user_query, (username, password))

    def delete_user_from_db(self, username, password):
        delete_user_query = "DELETE FROM users " \
                            "WHERE username = ? AND password = ?"
        self.execute_sql_query(delete_user_query, (username, password))

    def update_user_data(self, new_username, new_password, username, password):
        update_user_data_query = "UPDATE users " \
                                 "SET username = ?, password = ? " \
                                 "WHERE username = ? AND password = ?"
        self.execute_sql_query(update_user_data_query, (new_username, new_password, username, password))

    def user_messages_list(self, username, boolean_condition):
        user_messages_list_query = "SELECT sender, message_text FROM messages " \
                                   "WHERE user_id = (SELECT user_id FROM users WHERE username = ?) " \
                                   "AND archived = ? " \
                                   "ORDER BY message_date"
        messages_list = self.execute_sql_query(user_messages_list_query, (username, boolean_condition), fetch_option = "fetchall")
        return messages_list

    def save_message_to_db(self, sender, message, recipient):
            get_recipient_query = "SELECT user_id FROM users " \
                                  "WHERE username = ?"
            recipient_id = self.execute_sql_query(get_recipient_query, (recipient, ), fetch_option = "fetchone")
            message_save_query = "INSERT INTO messages (user_id, sender, message_text) " \
                                 "VALUES (?, ?, ?)"
            self.execute_sql_query(message_save_query, (recipient_id[0], sender, message))

    def archive_messages(self, username):
        archive_messages_query = "UPDATE messages " \
                                 "SET archived = True " \
                                 "WHERE user_id = (SELECT user_id FROM users WHERE username = ?)" \
                                 "AND archived = False"
        self.execute_sql_query(archive_messages_query, (username, ))

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

