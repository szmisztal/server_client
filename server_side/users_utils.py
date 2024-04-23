import os
from server_side.data_utils import DataUtils, SQLite
from config_variables import logger_config


sqlite_db_base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sqlite_database_path = os.path.join(sqlite_db_base_directory, "sqlite_server-client_db.db")


class User:

    def __init__(self):
        self.username = None
        self.__password = None
        self.admin_role = False
        self.data_utils = DataUtils()
        self.logger = logger_config("User", os.getcwd(), "server_logs.log")
        self.sqlite_utils = SQLite(sqlite_database_path)
        # self.postgresql_utils = PostgreSQL(**postgreSQL_server_connection_dict)

    def register_user(self, user_data):
        username = user_data["username"]
        try:
            validate_username = self.sqlite_utils.validate_username(username)
            if validate_username is False:
                password = user_data["password"]
                self.sqlite_utils.register_user_to_db(username, password)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def login_user(self, user_data):
        username, password = user_data["username"], user_data["password"]
        try:
            validate_data = self.sqlite_utils.validate_credentials(username, password)
            if validate_data:
                self.username, self.__password = username, password
            return validate_data
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def change_user_data(self, user_data):
        new_username = user_data["username"]
        try:
            validate_username = self.sqlite_utils.validate_username(new_username)
            if validate_username is False:
                new_password = user_data["password"]
                self.sqlite_utils.update_user_data(new_username, new_password, self.username)
                self.username, self.__password = new_username, new_password
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def delete_user(self, user_confirmation):
        if user_confirmation != "y":
            return False
        try:
            self.sqlite_utils.delete_user_from_db(self.username)
            return True
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def check_message_length(self, message):
        if len(message) > 255:
            return False
        return True

    def check_recipient_mailbox(self, recipient, unread_messages_bool):
        try:
            verify_recipient_mailbox = len(self.sqlite_utils.user_messages_list(recipient, unread_messages_bool))
            if verify_recipient_mailbox < 5:
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def send_message(self, data):
        recipient = data["recipient"]
        try:
            validate_recipient = self.sqlite_utils.validate_username(recipient)
            if validate_recipient:
                message = data["mail"]
                verify_message_length = self.check_message_length(message)
                verify_recipient_mailbox = self.check_recipient_mailbox(recipient, False)
                if verify_message_length and verify_recipient_mailbox:
                    self.sqlite_utils.save_message_to_db(recipient, self.username, message)
                    return True
                else:
                    return False
            return None
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def show_unread_messages(self):
        try:
            user_messages_list = self.sqlite_utils.user_messages_list(self.username, False)
            self.sqlite_utils.archive_messages(self.username)
            return user_messages_list
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return []

    def show_archived_messages(self):
        try:
            archived_messages = self.sqlite_utils.user_messages_list(self.username, True)
            return archived_messages
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return []

    def __str__(self):
        return f"Username: {self.username}, Admin role: {self.admin_role}"


