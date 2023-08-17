from datetime import datetime as dt
from variables import server_version, server_start_date
from data_utils import serialize_json

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

class User():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def register_user(cls):
        username = input("Choose your username: ")
        password = input("Set your password: ")
        return cls(username, password)

    def serialize_user_dict_to_json(self):
        user_dict = {
            f"{self.username}": f"{self.password}"
        }
        return serialize_json(user_dict)
