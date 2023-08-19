from datetime import datetime as dt
from variables import server_version, server_start_date, users_file
from data_utils import serialize_json, write_to_json_file


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
            "Register": "Register new user",
            "Uptime": "Shows the lifetime of the server",
            "Info": "Shows the current version and server start date",
            "Help": "Shows available commands",
            "Stop": "Shuts down the server"
        }
        return serialize_json(commands)

class User():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def serialize_user_to_dict(self):
        user_dict = {
            "username": self.username,
            "password": self.password
        }
        return user_dict

    @classmethod
    def register_user(cls, registration_data_dict):
        user = cls(**registration_data_dict)
        write_to_json_file(users_file, registration_data_dict)
        register_msg = {
            "Message": f"User: {user.username}, registered successfully"
        }
        return serialize_json(register_msg)






