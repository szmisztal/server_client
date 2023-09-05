from datetime import datetime as dt


class CommunicationUtils:
    def __init__(self, server):
        self.server = server
        self.commands_list = ["uptime", "info", "help", "stop"]

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

    def help(self):
        commands_dict = {
            "Uptime": "Shows the lifetime of the server",
            "Info": "Shows the current version and server start date",
            "Help": "Shows available commands",
            "Stop": "Shuts down the server"
        }
        return commands_dict

    def response_to_client(self, client_request):
        if client_request == "stop":
            return self.server.stop()
        elif client_request == "uptime":
            return self.uptime()
        elif client_request == "info":
            return self.info()
        elif client_request == "help":
            return self.help()
        else:
            error_message = {
                "Unknown command": f"'{client_request}', try again"
            }
            return error_message


# def request_to_server(client_request):
#     request = input("Choose command: uptime / info / help / show data / change data / send message / "
#                         "inbox / archived messages / logout / stop \n")
#         return request
#     else:
#         request = input("Choose command: register / login / stop \n")
#         return request
#
# def response_to_client(client_request, **kwargs):
#     if client_request == "uptime":
#         command = kwargs.get("command")
#         server_start_time = kwargs.get("server_start_time")
#         return command.uptime(server_start_time)
#     elif client_request == "info":
#         command = kwargs.get("command")
#         return command.info()
#     elif client_request == "help":
#         command = kwargs.get("command")
#         return command.help()
#     elif client_request in ["admin register", "register"]:
#         registration_data = kwargs.get("registration_data")
#         registration_data_dict = deserialize_json(registration_data)
#         return User.register_user(registration_data_dict)
#     elif client_request == "show data":
#         user = kwargs.get("user")
#         return user.show_current_data()
#     elif client_request  == "login":
#         user = kwargs.get("user")
#         login_data = kwargs.get("login_data")
#         login_data_dict = deserialize_json(login_data)
#         return user.login_user(login_data_dict)
#     elif client_request == "change data":
#         user = kwargs.get("user")
#         new_data = kwargs.get("new_data")
#         new_data_dict = deserialize_json(new_data)
#         return user.change_user_data(new_data_dict)
#     elif client_request == "send message":
#         user = kwargs.get("user")
#         recipient_data = kwargs.get("recipient_data")
#         message_data = kwargs.get("message_data")
#         if recipient_data and message_data:
#             recipient_data = deserialize_json(recipient_data)
#             message_data = deserialize_json(message_data)
#             return user.send_message(recipient_data, message_data)
#         elif recipient_data:
#             recipient_data = deserialize_json(recipient_data)
#             return serialize_json(recipient_data)
#     elif client_request == "inbox":
#         user = kwargs.get("user")
#         return user.show_new_messages()
#     elif client_request == "archived messages":
#         user = kwargs.get("user")
#         return user.show_archived_messages()
#     elif client_request == "logout":
#         command = kwargs.get("command")
#         return command.logout()
#     else:
#         error_msg = {
#             "Unknown command": f"'{client_request}', try again"
#         }
#         return serialize_json(error_msg)



