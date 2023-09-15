from data_utils import DataUtils


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.admin_role = False
        self.logged_in = False
        self.data_utils = DataUtils()
        self.users_file = "users_list.json"
        self.users_list = self.data_utils.read_json_file(self.users_file) or []

    def validate_username(self, username):
        for u in self.users_list:
            stored_username = u["username"]
            if stored_username == username:
                return False
        return True

    def validate_credentials(self, username, password):
        for u in self.users_list:
            stored_username = u["username"]
            stored_password = u["password"]
            if username == stored_username and password == stored_password:
                return True
        return False

    def add_user_to_list_and_write_to_file(self, user_data):
        self.users_list.append(user_data)
        self.data_utils.write_to_json_file(self.users_file, self.users_list)

    def register_user(self, user_data):
        username = user_data["username"]
        validated_username = self.validate_username(username)
        if validated_username == True:
            self.add_user_to_list_and_write_to_file(user_data)
            register_message = {
                f"User": f"{username} registered successfully",
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
        validated_data = self.validate_credentials(username, password)
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

    def show_data(self):
        show_data_message = {
            "Your current data: ": f"username: {self.username}, password: {self.password} "
        }
        return show_data_message

    def logout(self):
        logout_message = {
            "Logout": "You was successfully log out"
        }
        return logout_message

    def change_user_data(self, new_user_data):
        new_username = new_user_data["username"]
        new_password = new_user_data["password"]
        new_messages = self.data_utils.read_json_file(f"{self.username}_new_messages.json") or []
        archived_messages = self.data_utils.read_json_file(f"{self.username}_archived_messages.json") or []
        validated_username = self.validate_username(new_username)
        if validated_username == False:
            error_message = {
                "Username": "In use, choose another"
            }
            return error_message
        else:
            for u in self.users_list:
                if self.username == u["username"]:
                    u["username"] = self.username = new_username
                    u["password"] = self.password = new_password
                    self.data_utils.write_to_json_file(self.users_file, self.users_list)
                    self.data_utils.write_to_json_file(f"{self.username}_new_messages.json", new_messages)
                    self.data_utils.write_to_json_file(f"{self.username}_archived_messages.json", archived_messages)
                    change_data_message = {
                        "Success": f"Your new data: username: {self.username}, password: {self.password}"
                    }
                    return change_data_message

    def send_message(self, recipient_data, message_data):
        recipient = recipient_data
        message = message_data
        validated_recipient = self.validate_username(recipient)
        if validated_recipient == True:
            error_message = {
                "Recipient": "User not found, try again"
            }
            return error_message
        else:
            recipient_messages = self.data_utils.read_json_file(f"{recipient}_new_messages.json") or []
            if len(message) > 255:
                error_message = {
                    "Failed": "Max message length = 255"
                }
                return error_message
            elif len(recipient_messages) >= 5:
                if self.admin_role == False:
                    error_message = {
                        "Failed": "Recipient`s mailbox is full"
                    }
                    return error_message
                else:
                    pass
            else:
                message_data_dict = {
                    "Message from": self.username,
                    "Text": message
                }
                recipient_messages.append(message_data_dict)
                self.data_utils.write_to_json_file(f"{recipient}_new_messages.json", recipient_messages)
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
        archived_messages = self.data_utils.read_json_file(f"{self.username}_archived_messages.json")
        return archived_messages

    def __str__(self):
        return f"Username:{self.username}, Password: {self.password}, Login status: {self.logged_in}, Admin role: {self.admin_role}"


