import json
import bcrypt
import psycopg2
from config_variables import encode_format


class DataUtils:
    """
    A utility class for data-related operations such as password hashing,
    and reading/writing JSON files.

    Attributes:
    ----------
    encode_format : str
        The format used for encoding strings.
    """

    def __init__(self):
        """
        Initializes the DataUtils with the specified encoding format.
        """
        self.encode_format = encode_format

    def hash_password(self, raw_password):
        """
        Hashes a raw password using bcrypt.

        Parameters:
        ----------
        raw_password : str
            The raw password to hash.

        Returns:
        -------
        bytes
            The hashed password.
        """
        password = raw_password.encode(self.encode_format)
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password

    def check_hashed_password(self, raw_password, hashed_password):
        """
        Checks if a raw password matches the hashed password.

        Parameters:
        ----------
        raw_password : str
            The raw password to check.
        hashed_password : str
            The hashed password to check against.

        Returns:
        -------
        bool
            True if the password matches, False otherwise.
        """
        password = raw_password.encode(self.encode_format)
        hashed_password = bytes.fromhex(hashed_password.replace("\\x", ""))
        validate_password = bcrypt.checkpw(password, hashed_password)
        return validate_password

    def write_to_json_file(self, filename, data):
        """
        Writes data to a JSON file.

        Parameters:
        ----------
        filename : str
            The name of the file to write to.
        data : dict
            The data to write to the file.
        """
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def read_json_file(self, filename):
        """
        Reads data from a JSON file.

        Parameters:
        ----------
        filename : str
            The name of the file to read from.

        Returns:
        -------
        dict
            The data read from the file.
        """
        try:
            with open(filename, "r") as file:
                users_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users_data = []
        return users_data


class PostgreSQL:
    """
    A class to handle PostgreSQL database operations.

    Attributes:
    ----------
    user : str
        The database user.
    password : str
        The database password.
    host : str
        The database host.
    port : int
        The database port.
    database : str
        The database name.
    data_utils : DataUtils
        Utility for data-related operations.
    """

    def __init__(self, user, password, host, port, database):
        """
        Initializes the PostgreSQL with the specified connection parameters.

        Parameters:
        ----------
        user : str
            The database user.
        password : str
            The database password.
        host : str
            The database host.
        port : int
            The database port.
        database : str
            The database name.
        """
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.data_utils = DataUtils()
        self.initialize_db()

    def initialize_db(self):
        """
        Initializes the database by creating necessary tables.
        """
        with self.connection_to_db() as conn:
            with conn.cursor() as cursor:
                self.create_user_table(cursor)
                self.create_message_table(cursor)

    def connection_to_db(self):
        """
        Establishes a connection to the PostgreSQL database.

        Returns:
        -------
        connection : psycopg2.connection
            The database connection.

        Raises:
        -------
        psycopg2.Error
            If the connection to the database fails.
        """
        try:
            connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return connection
        except psycopg2.Error as e:
            print(f"Failed to connect to the database: {e}")
            raise e

    def execute_sql_query(self, query, params=None, fetch_option=None):
        """
        Executes an SQL query on the database.

        Parameters:
        ----------
        query : str
            The SQL query to execute.
        params : tuple, optional
            The parameters for the SQL query.
        fetch_option : str, optional
            The fetch option for the query results ('fetchone' or 'fetchall').

        Returns:
        -------
        result : tuple or list
            The query result based on the fetch option.

        Raises:
        -------
        psycopg2.Error
            If an error occurs while executing the query.
        """
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
        """
        Checks if a table exists in the database.

        Parameters:
        ----------
        table_name : str
            The name of the table to check.
        cursor : psycopg2.cursor
            The database cursor.

        Returns:
        -------
        bool
            True if the table exists, False otherwise.
        """
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
        cursor.execute(query)
        return cursor.fetchone()[0]

    def create_user_table(self, cursor):
        """
        Creates the 'users' table if it does not exist.

        Parameters:
        ----------
        cursor : psycopg2.cursor
            The database cursor.
        """
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
        """
        Creates the 'messages' table if it does not exist.

        Parameters:
        ----------
        cursor : psycopg2.cursor
            The database cursor.
        """
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
        """
        Validates if the username exists in the database.

        Parameters:
        ----------
        username : str
            The username to validate.

        Returns:
        -------
        bool
            True if the username exists, False otherwise.
        """
        query = "SELECT username FROM users WHERE username = %s"
        existing_username = self.execute_sql_query(query, (username,), fetch_option="fetchone")
        if existing_username is not None:
            return True
        return False

    def get_hashed_password_from_db(self, username):
        """
        Retrieves the hashed password for a given username from the database.

        Parameters:
        ----------
        username : str
            The username to retrieve the hashed password for.

        Returns:
        -------
        str
            The hashed password.
        """
        query = "SELECT password FROM users WHERE username = %s"
        hashed_password = self.execute_sql_query(query, (username,), fetch_option="fetchone")
        return hashed_password[0]

    def validate_credentials(self, username, password):
        """
        Validates the user's credentials.

        Parameters:
        ----------
        username : str
            The username to validate.
        password : str
            The raw password to validate.

        Returns:
        -------
        bool
            True if the credentials are valid, False otherwise.
        """
        hashed_password = self.get_hashed_password_from_db(username)
        validate_password = self.data_utils.check_hashed_password(password, hashed_password)
        if validate_password:
            return True
        return False

    def register_user_to_db(self, username, raw_password):
        """
        Registers a new user in the database.

        Parameters:
        ----------
        username : str
            The username of the new user.
        raw_password : str
            The raw password of the new user.
        """
        hashed_password = self.data_utils.hash_password(raw_password)
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.execute_sql_query(query, (username, hashed_password))

    def update_user_data(self, new_username, new_password, username):
        """
        Updates the user's data in the database.

        Parameters:
        ----------
        new_username : str
            The new username.
        new_password : str
            The new raw password.
        username : str
            The current username.
        """
        new_hashed_password = self.data_utils.hash_password(new_password)
        query = "UPDATE users SET username = %s, password = %s WHERE username = %s"
        self.execute_sql_query(query, (new_username, new_hashed_password, username))

    def delete_user_from_db(self, username):
        """
        Deletes a user from the database.

        Parameters:
        ----------
        username : str
            The username of the user to delete.
        """
        hashed_password = self.get_hashed_password_from_db(username)
        query = "DELETE FROM users WHERE username = %s AND password = %s"
        self.execute_sql_query(query, (username, hashed_password))

    def get_recipient_id(self, recipient_username):
        """
        Retrieves the user ID for a given recipient username.

        Parameters:
        ----------
        recipient_username : str
            The recipient's username.

        Returns:
        -------
        int
            The user ID of the recipient.
        """
        query = "SELECT user_id FROM users WHERE username = %s"
        return self.execute_sql_query(query, (recipient_username,), fetch_option="fetchone")

    def save_message_to_db(self, recipient, sender, message):
        """
        Saves a message to the database.

        Parameters:
        ----------
        recipient : str
            The recipient's username.
        sender : str
            The sender's username.
        message : str
            The message text.
        """
        recipient_id = self.get_recipient_id(recipient)
        message_save_query = "INSERT INTO messages (user_id, sender, message_text) VALUES (%s, %s, %s)"
        self.execute_sql_query(message_save_query, (recipient_id[0], sender, message))

    def user_messages_list(self, username, boolean_condition):
        """
        Retrieves the list of messages for a user based on the archived condition.

        Parameters:
        ----------
        username : str
            The username of the recipient.
        boolean_condition : bool
            The condition to filter archived messages.

        Returns:
        -------
        list
            A list of messages.
        """
        query = "SELECT sender, message_text FROM messages WHERE user_id = (SELECT user_id FROM users WHERE username = %s) " \
                "AND archived = %s ORDER BY message_date"
        messages_list = self.execute_sql_query(query, (username, boolean_condition), fetch_option="fetchall")
        return messages_list

    def archive_messages(self, username):
        """
        Archives the user's messages.

        Parameters:
        ----------
        username : str
            The username of the user whose messages are to be archived.
        """
        query = "UPDATE messages SET archived = True WHERE user_id = (SELECT user_id FROM users WHERE username = %s) AND archived = False"
        self.execute_sql_query(query, (username,))



