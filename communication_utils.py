from datetime import datetime as dt


class CommunicationUtils:
    def __init__(self, server):
        self.server = server
        self.commands_list = [
            "uptime",
            "info",
            "help",
            "stop",
            "register",
            "login",
            "show data",
            "change data",
            "send message",
            "mailbox",
            "archives",
            "logout"
        ]

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
        if user.logged_in == True:
            commands_dict = {
                "Uptime": "Shows the lifetime of the server",
                "Info": "Shows the current version and server start date",
                "Help": "Shows available commands",
                "Show data": "Shows your user data",
                "Change data": "Change your current user data",
                "Send message": "Send message to another user",
                "Mailbox": "Read new messages",
                "Archives": "Read archived messages",
                "Logout": "Sign out the user",
                "Stop": "Shuts down the server",
            }
        else:
            commands_dict = {
                "Register": "Sign up new user",
                "Login": "Sign in the user",
                "Stop": "Shuts down the server"
            }
        return commands_dict

    def unknown_command(self, client_request):
        if client_request not in self.commands_list:
            error_message = {
                "Unknown command": f"'{client_request}', try again"
            }
            return error_message

    def response_to_client(self, client_request, user):
        if user.logged_in == True:
            if client_request == "uptime":
                return self.uptime()
            elif client_request == "info":
                return self.info()
            elif client_request == "help":
                return self.help(user)
            elif client_request == "show data":
                return user.show_data()
            elif "New data" in client_request:
                user_data = client_request["New data"]
                return user.change_user_data(user_data)
            elif "Recipient" and "Message" in client_request:
                recipient_data = client_request["Recipient"]
                message_data = client_request["Message"]
                return user.send_message(recipient_data, message_data)
            elif client_request == "mailbox":
                return user.show_new_messages()
            elif client_request == "archives":
                return user.show_archived_messages()
            elif client_request == "logout":
                return user.logout()
            elif client_request == "stop":
                return self.server.stop()
            else:
                return self.unknown_command(client_request)
        else:
            if "Register" in client_request:
                user_data = client_request["Register"]
                return user.register_user(user_data)
            elif "Login" in client_request:
                user_data = client_request["Login"]
                return user.login_user(user_data)
            elif client_request == "help":
                return self.help(user)
            elif client_request == "stop":
                return self.server.stop()
            else:
                error_message = {
                    "Error": "You have to sign in first to see available commands"
                }
                return error_message






