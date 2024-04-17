from datetime import datetime as dt


class MessageTemplate:
    def __init__(self, instance):
        self.instance = instance

    def template(self, message = None, data = None):
        template = {
            "status": self.instance,
            "message": message,
            "data": data,
        }
        return template


class ServerResponses:
    def __init__(self, server):
        self.server = server
        self.message_template = MessageTemplate("RESPONSE")
        self.commands_list = [
            "uptime",
            "info",
            "help",
            "stop",
            "register",
            "login",
            "change data",
            "send message",
            "mailbox",
            "archives",
            "logout",
            "delete"
        ]

    def welcome_message(self):
        return self.message_template.template(message = "Type 'help' to see available commands")

    def uptime(self):
        current_time = dt.now()
        server_uptime = current_time - self.server.server_start_time
        return self.message_template.template(message = f"Server uptime - {server_uptime}")

    def info(self):
        server_info_dict = {
            "Server start date:": self.server.server_start_date,
            "Server version:": self.server.server_version
        }
        return self.message_template.template(message = server_info_dict)

    def help(self):
        commands_dict = {
            "Uptime": "Shows the lifetime of the server",
            "Info": "Shows the current version and server start date",
            "Help": "Shows available commands",
            "Change data": "Change your current user data",
            "Send message": "Send message to another user",
            "Mailbox": "Read new messages",
            "Archives": "Read archived messages",
            "Logout": "Sign out the user",
            "Delete": "Delete your data from database",
            "Stop": "Shuts down the server",
        }
    # else:
    #     commands_dict = {
    #         "Register": "Sign up new user",
    #         "Login": "Sign in the user",
    #         "Stop": "Shuts down the server"
    #     }
        return self.message_template.template(message = commands_dict)

    def unknown_command(self, client_request):
        return self.message_template.template(message = f"Unknown command - '{client_request}', try again")

    def response_to_client(self, client_request):
        if client_request not in self.commands_list:
            return self.unknown_command(client_request)
        if client_request == "uptime":
            return self.uptime()
        elif client_request == "info":
            return self.info()
        elif client_request == "help":
            return self.help()
        #     elif "New data" in client_request:
        #         user_data = client_request["New data"]
        #         return user.change_user_data(user_data)
        #     elif "Recipient" and "Message" in client_request:
        #         recipient_data = client_request["Recipient"]
        #         message_data = client_request["Message"]
        #         return user.send_message(recipient_data, message_data)
        #     elif client_request == "mailbox":
        #         return user.show_new_messages()
        #     elif client_request == "archives":
        #         return user.show_archived_messages()
        #     elif client_request == "logout":
        #         return user.logout()
        #     elif "Delete confirmation" in client_request:
        #         user_confirmation = client_request["Delete confirmation"]
        #         return user.delete_user(user_confirmation)
        #     elif client_request == "stop":
        #         return self.server.stop()
        #     else:
        #         return self.unknown_command(client_request)
        # else:
        #     if "Register" in client_request:
        #         user_data = client_request["Register"]
        #         return user.register_user(user_data)
        #     elif "Login" in client_request:
        #         user_data = client_request["Login"]
        #         return user.login_user(user_data)
        #     elif client_request == "help":
        #         return self.help(user)
        #     elif client_request == "stop":
        #         return self.server.stop()
        #     else:
        #         error_message = {
        #             "Error": "You have to sign in first to see available commands"
        #         }
        #         return error_message


class ClientRequests:
    def __init__(self):
        self.message_template = MessageTemplate("REQUEST")

    def command_input(self):
        command = input("REQUEST: ").lower()
        return self.message_template.template(message = command)

    def user_data_input(self):
        username = input("Username: ")
        password = input("Password: ")
        user_data = {
            "username": username,
            "password": password
        }
        return user_data

    def register_user(self):
        user_data = self.user_data_input()
        return self.message_template.template(message = "REGISTER", data = user_data)




