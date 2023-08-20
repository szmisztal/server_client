from datetime import datetime as dt
from variables import server_version, server_start_date, users_file
from data_utils import serialize_json, write_to_json_file, read_json_file


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
        self.logged_in = False

    @classmethod
    def register_user(cls, registration_data_dict):
        username = registration_data_dict["username"]
        users_list = read_json_file(users_file)
        for user_data in users_list:
            stored_username = user_data["username"]
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

    def is_logged_in(self):
        return self.logged_in

    def __str__(self):
        return f"{self.username}, {self.password}, {self.logged_in}"





