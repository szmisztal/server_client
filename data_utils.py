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
        try:
            cursor = connection.cursor()
            table_status = self.check_that_table_exist(cursor, "users")
            if table_status == True:
                create_table_query = '''CREATE TABLE users(
                                    user_id SERIAL PRIMARY KEY,
                                    username VARCHAR NOT NULL,
                                    password VARCHAR NOT NULL,
                                    sign_up_date DATE NOT NULL DEFAULT CURRENT_DATE,
                                    admin_role BOOLEAN NOT NULL DEFAULT FALSE
                                    )'''
                cursor.execute(create_table_query)
                connection.commit()
                print("TABLE 'users' CREATED...")
            else:
                print("TABLE 'users' EXISTS...")
        except psycopg2.Error as e:
            print(f"Error: {e}")
        finally:
            connection.close()

    def create_message_table(self):
        connection = self.connection_to_db()
        try:
            cursor = connection.cursor()
            table_status = self.check_that_table_exist(cursor, "messages")
            if table_status == True:
                create_table_query = '''CREATE TABLE messages(
                                    message_id SERIAL PRIMARY KEY,
                                    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                                    sender VARCHAR NOT NULL,
                                    message_date DATE NOT NULL DEFAULT CURRENT_DATE,
                                    message_text VARCHAR(255) NOT NULL,
                                    archived BOOLEAN NOT NULL DEFAULT FALSE
                                    )'''
                cursor.execute(create_table_query)
                connection.commit()
                print("TABLE 'messages' CREATED")
            else:
                print("TABLE 'messages' EXISTS")
        except psycopg2.Error as e:
            print(f"Error: {e}")
        finally:
            connection.close()

    def validate_username(self, username):
        connection = self.connection_to_db()
        try:
            cursor = connection.cursor()
            users_query = "SELECT username FROM users WHERE username = %s"
            cursor.execute(users_query, (username, ))
            existing_username = cursor.fetchone()
            if existing_username is not None:
                return False
            else:
                return True
        except psycopg2.Error as e:
            print(f"Error: {e}")
            return False
        finally:
            connection.close()

    def validate_credentials(self, username, password):
        connection = self.connection_to_db()
        try:
            cursor = connection.cursor()
            users_query = "SELECT username, password FROM users WHERE username = %s AND password = %s"
            cursor.execute(users_query, (username, password))
            credentials = cursor.fetchone()
            if credentials is not None:
                return True
            else:
                return False
        except psycopg2.Error as e:
            print(f"Error: {e}")
            return False
        finally:
            connection.close()

    def register_user_to_db(self, username, password):
        connection = self.connection_to_db()
        try:
            cursor = connection.cursor()
            insert_user_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(insert_user_query, (username, password))
            connection.commit()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            connection.close()

    def delete_user_from_db(self, username, password):
        connection = self.connection_to_db()
        try:
            cursor = connection.cursor()
            delete_user_query = "DELETE FROM users WHERE username = %s AND password = %s"
            cursor.execute(delete_user_query, (username, password))
            connection.commit()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            connection.close()

    def update_user_data(self, new_username, new_password, username, password):
        connection = self.connection_to_db()
        try:
            cursor = connection.cursor()
            update_data_query = "UPDATE users SET username = %s, password = %s WHERE username = %s AND password = %s"
            cursor.execute(update_data_query, (new_username, new_password, username, password))
            connection.commit()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            connection.close()

    def user_messages_list(self, username, boolean_condition):
        connection = self.connection_to_db()
        try:
            cursor = connection.cursor()
            messages_list_query = "SELECT sender, message_date, message_text FROM messages " \
                                  "WHERE user_id = (SELECT user_id FROM users WHERE username = %s)" \
                                  "AND archived = %s ORDER BY message_date"
            cursor.execute(messages_list_query, (username, boolean_condition))
            messages_list = cursor.fetchall()
            return messages_list
        except psycopg2.Error as e:
            print(f"Error: {e}")
            messages_list = []
            return messages_list
        finally:
            connection.close()

    def save_message_to_db(self, sender, message, recipient):
        connection = self.connection_to_db()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (recipient, ))
            recipient_id = cursor.fetchone()
            message_save_query = "INSERT INTO messages (user_id, sender, message_text) VALUES (%s, %s, %s)"
            cursor.execute(message_save_query, (recipient_id[0], sender, message))
            cursor.commit()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            connection.close()

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
