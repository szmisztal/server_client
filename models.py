from datetime import datetime as dt
from variables import server_version, server_start_date, users_file
from data_utils import serialize_json, write_to_json_file, read_json_file


users_list = read_json_file(users_file) or []

class Command():

    def uptime(self, server_start_time):
        current_time = dt.now()
        server_uptime = current_time - server_start_time
        uptime_dict = {
            "Server uptime time": f"{server_uptime}"
        }
        return serialize_json(uptime_dict)

    def info(self):
        server_info = {
            "Server start date:": server_start_date,
            "Server version:": server_version
        }
        return serialize_json(server_info)

    def help(self):
        commands = {
            "Uptime": "Shows the lifetime of the server",
            "Info": "Shows the current version and server start date",
            "Help": "Shows available commands",
            "Show data": "Shows your current user-data",
            "Change data": "Change your user-data",
            "Send message": "Send message to other user",
            "Inbox": "Shows messages in your inbox",
            "Stop": "Shuts down the server"
        }
        return serialize_json(commands)

    def logout(self):
        logout_msg = {
            "Message": "You was logged out"
        }
        return serialize_json(logout_msg)


class User():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user_messages = []
        self.logged_in = False

    @classmethod
    def register_user(cls, registration_data_dict):
        username = registration_data_dict["username"]
        for u in users_list:
            stored_username = u["username"]
            if username == stored_username:
                error_msg = {
                    "Username": "In use, choose another"
                }
                return serialize_json(error_msg)
        user = cls(**registration_data_dict)
        user_dict = {
            "username": user.username,
            "password": user.password
        }
        users_list.append(user_dict)
        write_to_json_file(users_file, users_list)
        register_msg = {
            "Message": f"User: {user.username}, registered successfully"
        }
        return serialize_json(register_msg)

    def login_user(self, login_data_dict):
        self.username = login_data_dict["username"]
        self.password = login_data_dict["password"]
        for u in users_list:
            stored_username = u["username"]
            stored_password = u["password"]
            if self.username == stored_username and self.password == stored_password:
                login_msg = {
                    "Message": "You was logged in"
                }
                return serialize_json(login_msg)
        error_msg = {
            "Message": "Incorrect data. try again"
        }
        return serialize_json(error_msg)

    def is_logged_in(self):
        return self.logged_in

    def show_current_data(self):
        current_data_msg = {
            "Your current username and password:": f"Username: {self.username}, password: {self.password}"
        }
        return serialize_json(current_data_msg)

    def change_user_data(self, new_data_dict):
        new_username = new_data_dict["username"]
        new_password = new_data_dict["password"]
        for u in users_list:
            stored_username = u["username"]
            if stored_username == new_username and stored_username != self.username:
                error_msg = {
                    "Username": "In use, choose another"
                }
                return serialize_json(error_msg)
        for u in users_list:
            if self.username == u["username"]:
                u["username"] = self.username = new_username
                u["password"] = self.password = new_password
                write_to_json_file(users_file, users_list)
                success_msg = {
                    "Success": f"Your new data: username = {self.username}, password = {self.password}"
                }
                return serialize_json(success_msg)

    def send_message(self,  recipient_data, message_data):
        message = message_data["message"]
        recipient = User(**recipient_data)
        if len(message) > 255:
            print("Max message length = 255")
        elif len(recipient.user_messages) >= 5:
            print("Inbox full")
        else:
            message_dict = {
                "Message from": self.username,
                "Message to": recipient.username,
                "Text": message
            }
            recipient.user_messages.append(message_data)
            write_to_json_file(f"{recipient.username}_messages.json", message_dict)
            success_msg = {
                "Message": "Message send successfully"
            }
            return serialize_json(success_msg)

    def show_messages(self):
        user_messages = read_json_file(f"{self.username}.messages.json")
        for m in user_messages:
            print(m)

    def __str__(self):
        return f"{self.username}, {self.password}, {self.logged_in}"



def user_username_and_password_input():
    username = input("Username: ")
    password = input("Password: ")
    user_data = {
        "username": username,
        "password": password
    }
    return user_data

def recipient_input():
    recipient = input("Who do you want to send a message to ?: ")
    for u in users_list:
        if recipient == u["username"]:
            recipient_data = {
                "username": u["username"],
                "password": u["password"]
            }
            return recipient_data
    else:
        error_msg ={
            "Error": "User not found"
        }
        return error_msg

def message_input():
    message = input("Write a message: ")
    message_data = {
        "message": message
    }
    return message_data



