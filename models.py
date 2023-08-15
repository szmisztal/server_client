from datetime import datetime as dt
from variables import server_version, server_start_date, server_start_time
from data_utils import serialize_json

class Command():

    def __init__(self, client_request):
        self.client_request = client_request

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

    def stop(self):
        stop_msg = {
            "Server status": "Shutting down"
        }
        return serialize_json(stop_msg)

    def response_to_client(self, client_request):
        if client_request == "uptime":
            return self.uptime(server_start_time)
        elif client_request == "info":
            return self.info()
        elif client_request == "help":
            return self.help()
        elif client_request == "stop":
            return self.stop()
        else:
            error_msg = {
                "Unknown command": f"'{client_request}', try again"
            }
            return serialize_json(error_msg)
