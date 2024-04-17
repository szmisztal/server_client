from server_side.data_utils import DataUtils, SQLite
from config_variables import sqlite_database_path, postgreSQL_server_connection_dict


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
        if validate_username == True:
            password = user_data["password"]
            self.sqlite_utils.register_user_to_db(username, password)
        return validate_username

    def login_user(self, user_data):
        username, password = user_data["username"], user_data["password"]
        validate_data = self.sqlite_utils.validate_credentials(username, password)
        if validate_data:
            self.username, self.__password = username, password
        return validate_data

    def change_user_data(self, new_user_data):
        new_username = new_user_data["username"]
        new_password = new_user_data["password"]
        new_hashed_password = self.data_utils.hash_password(new_password)
        validated_username = self.sqlite_utils.validate_username(new_username)
        if validated_username == False:
            error_message = {
                "Username": "In use, choose another"
            }
            return error_message
        else:
            hashed_password = self.sqlite_utils.get_hashed_password_from_db(self.username)
            self.sqlite_utils.update_user_data(new_username, new_hashed_password, self.username, hashed_password)
            change_data_message = {
                "Success": f"Your new data: username: {new_username}, password: {new_password}"
            }
            return change_data_message

    def delete_user(self, user_confirmation):
        if user_confirmation != "yes":
            not_deletion_message = {
                "Confirmation failed": "Your data will remain in the database"
            }
            return not_deletion_message
        else:
            hashed_password = self.sqlite_utils.get_hashed_password_from_db(self.username)
            self.sqlite_utils.delete_user_from_db(self.username, hashed_password)
            deletion_message = {
                "Delete": "You have been deleted from database"
            }
            return deletion_message

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


