import os
from data_utils import DataUtils, SQLite


sqlite_db_base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sqlite_database_path = os.path.join(sqlite_db_base_directory, "sqlite_server-client_db.db")


class User:

    def __init__(self):
        self.username = None
        self.__password = None
        self.admin_role = False
        self.data_utils = DataUtils()
        self.sqlite_utils = SQLite(sqlite_database_path)
        # self.postgresql_utils = PostgreSQL(**postgreSQL_server_connection_dict)

    def register_user(self, user_data):
        username = user_data["username"]
        validate_username = self.sqlite_utils.validate_username(username)
        if validate_username is True:
            password = user_data["password"]
            self.sqlite_utils.register_user_to_db(username, password)
        return validate_username

    def login_user(self, user_data):
        username, password = user_data["username"], user_data["password"]
        validate_data = self.sqlite_utils.validate_credentials(username, password)
        if validate_data:
            self.username, self.__password = username, password
        return validate_data

    def change_user_data(self, user_data):
        new_username = user_data["username"]
        validate_username = self.sqlite_utils.validate_username(new_username)
        if validate_username is True:
            new_password = user_data["password"]
            self.sqlite_utils.update_user_data(new_username, new_password, self.username)
            self.username, self.__password = new_username, new_password
        return validate_username

    def delete_user(self, user_confirmation):
        if user_confirmation != "y":
            return False
        self.sqlite_utils.delete_user_from_db(self.username)
        return True

    def send_message(self, recipient_data, message_data):
        recipient = recipient_data
        message = message_data
        validated_recipient = self.sqlite_utils.validate_username(recipient)
        if validated_recipient == True:
            error_message = {
                "Recipient": "User not found, try again"
            }
            return error_message
        else:
            recipient_messages_list = self.sqlite_utils.user_messages_list(recipient, False)
            if len(message) > 255:
                error_message = {
                    "Failed": "Max message length = 255"
                }
                return error_message
            elif len(recipient_messages_list) >= 5:
                if self.admin_role == False:
                    error_message = {
                        "Failed": "Recipient`s mailbox is full"
                    }
                    return error_message
            else:
                self.sqlite_utils.save_message_to_db(self.username, message, recipient)
                send_message_success = {
                    "Message": "Send successfully"
                }
                return send_message_success

    def show_new_messages(self):
        user_messages_list = self.sqlite_utils.user_messages_list(self.username, False)
        self.sqlite_utils.archive_messages(self.username)
        return user_messages_list

    def show_archived_messages(self):
        archived_messages = self.sqlite_utils.user_messages_list(self.username, True)
        return archived_messages

    def __str__(self):
        return f"Username: {self.username}, Password: {self.__password}, Admin role: {self.admin_role}"


