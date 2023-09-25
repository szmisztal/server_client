from data_utils import DataUtils


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.admin_role = False
        self.logged_in = False
        self.data_utils = DataUtils()

    def register_user(self, user_data):
        username = user_data["username"]
        password = user_data["password"]
        validated_username = self.data_utils.validate_username(username)
        if validated_username == True:
            self.data_utils.register_user_to_db(username, password)
            register_message = {
                "User": f"{username} registered successfully",
            }
            return register_message
        else:
            error_message = {
                "Username": "In use, choose another"
            }
            return error_message

    def login_user(self, user_data):
        username = user_data["username"]
        password = user_data["password"]
        validated_data = self.data_utils.validate_credentials(username, password)
        if validated_data == True:
            login_message = {
                f"User '{username}'": "Sign in successfully"
            }
            return login_message
        else:
            error_message = {
                "Incorrect data": "Try again"
            }
            return error_message

    def logout(self):
        logout_message = {
            "Logout": "You was successfully log out"
        }
        return logout_message

    def delete_user(self, user_confirmation):
        if user_confirmation not in ["yes", "Yes"]:
            not_deletion_message = {
                "Message": "Your data will remain in the database"
            }
            return not_deletion_message
        else:
            self.data_utils.delete_user_from_db(self.username, self.password)
            deletion_message = {
                "Success": "You have been deleted from database"
            }
            return deletion_message

    def change_user_data(self, new_user_data):
        new_username = new_user_data["username"]
        new_password = new_user_data["password"]
        validated_username = self.data_utils.validate_username(new_username)
        if validated_username == False:
            error_message = {
                "Username": "In use, choose another"
            }
            return error_message
        else:
            self.data_utils.update_user_data(new_username, new_password, self.username, self.password)
            change_data_message = {
                "Success": f"Your new data: username: {new_username}, password: {new_password}"
            }
            return change_data_message

    def send_message(self, recipient_data, message_data):
        recipient = recipient_data
        message = message_data
        validated_recipient = self.data_utils.validate_username(recipient)
        if validated_recipient == False:
            error_message = {
                "Recipient": "User not found, try again"
            }
            return error_message
        else:
            recipient_messages_list = self.data_utils.user_messages_list(recipient, False)
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
                self.data_utils.save_message_to_db(self.username, message, recipient)
                send_message_success = {
                    "Message": "Send successfully"
                }
                return send_message_success

    def show_new_messages(self):
        new_messages = self.data_utils.read_json_file(f"{self.username}_new_messages.json") or []
        messages_to_read = new_messages.copy()
        archived_messages = self.data_utils.read_json_file(f"{self.username}_archived_messages.json")
        archived_messages.extend(new_messages)
        new_messages = []
        self.data_utils.write_to_json_file(f"{self.username}_new_messages.json", new_messages)
        self.data_utils.write_to_json_file(f"{self.username}_archived_messages.json", archived_messages)
        return messages_to_read

    def show_archived_messages(self):
        archived_messages = self.data_utils.user_messages_list(self.username, True)
        return archived_messages

    def __str__(self):
        return f"Username: {self.username}, Password: {self.password}, Login status: {self.logged_in}, Admin role: {self.admin_role}"


