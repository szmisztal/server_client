from datetime import datetime as dt
from users_utils import User


class CommunicationUtils:
    def __init__(self, server):
        self.server = server
        self.user = User("", "")
        self.commands_list = ["uptime", "info", "help", "stop", "register", "login"]

    def uptime(self):
        current_time = dt.now()
        server_uptime = current_time - self.server.server_start_time
        uptime_dict = {
            "Server uptime time": f"{server_uptime}"
        }
        return uptime_dict

    def info(self):
        server_info_dict = {
            "Server start date:": self.server.server_start_date,
            "Server version:": self.server.server_version
        }
        return server_info_dict

    def help(self, user):
        login_status = user["login_status"]
        if login_status == "True":
            commands_dict = {
                "Uptime": "Shows the lifetime of the server",
                "Info": "Shows the current version and server start date",
                "Help": "Shows available commands",
                "Stop": "Shuts down the server"
            }
            return commands_dict
        elif login_status == "False" or login_status == None:
            commands_dict = {
                "Register": "Register new user",
                "Login": "Sign in",
                "Stop": "Shuts down the server"
            }
            return commands_dict

    def unknown_command(self, client_request):
        if client_request not in self.commands_list:
            error_message = {
                "Unknown command": f"'{client_request}', try again"
            }
            return error_message

    def response_to_client(self, **kwargs):
        client_request = kwargs.get("client_request")
        user = kwargs.get("user")
        if client_request == "stop":
            return self.server.stop()
        elif client_request == "uptime":
            return self.uptime()
        elif client_request == "info":
            return self.info()
        elif client_request == "help":
            return self.help(user)
        elif "Register" in client_request:
            return self.user.register_user(user)
        elif "Login" in client_request:
            return self.user.login_user(user)
        else:
            return self.unknown_command(client_request)




