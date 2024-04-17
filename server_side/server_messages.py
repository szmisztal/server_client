from datetime import datetime as dt
from server_side.users_utils import User


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
        self.user = User()
        self.user_logging_status = False
        self.user_username = None
        self.commands_list_for_logged_in_user = [
            "uptime",
            "info",
            "help",
            "stop",
            "change data",
            "send message",
            "mailbox",
            "archives",
            "logout",
            "delete"
        ]
        self.commands_list_for_not_logged_in_user = [
            "help",
            "register",
            "login",
            "stop"
        ]
        self.all_commands_list = set(self.commands_list_for_not_logged_in_user + self.commands_list_for_logged_in_user)

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
        if self.user_logging_status:
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
        else:
            commands_dict = {
                "Help": "Shows available commands",
                "Register": "Sign up new user",
                "Login": "Sign in the user",
                "Stop": "Shuts down the server"
            }
        return self.message_template.template(message = commands_dict)

    def stop_command(self):
        return self.message_template.template(message = "Server`s shutting down...")

    def unknown_command(self, client_request):
        return self.message_template.template(message = f"Unknown command - '{client_request}', try again")

    def forbidden_command_for_not_logged_in_user(self):
        return self.message_template.template(message = "You have to sign in first")

    def forbidden_command_for_logged_in_user(self):
        return self.message_template.template(message = "If you want to register new account or log in once more - log out first")

    def user_register_successfully(self):
        return self.message_template.template(message = "You are registered successfully")

    def user_register_failed(self):
        return self.message_template.template(message = "Username in use, choose another one")

    def user_sign_in_successfully(self):
        return self.message_template.template(message = "You are logged in successfully")

    def wrong_credentials(self):
        return self.message_template.template(message = "Wrong username or password, try again")

    def handling_register_command(self, user_data):
        verify_username = self.user.register_user(user_data)
        if verify_username is True:
            return self.user_register_successfully()
        return self.user_register_failed()

    def handling_login_command(self, user_data):
        verify_credentials = self.user.login_user(user_data)
        if verify_credentials:
            self.user_username = user_data["username"]
            self.user_logging_status = True
            return self.user_sign_in_successfully()
        return self.wrong_credentials()

    def handling_logout_command(self):
        self.user_logging_status = False
        return self.message_template.template(message = "You were log out successfully")

    def handling_commands_for_not_logged_in_user(self, command, data):
        if command not in self.commands_list_for_not_logged_in_user and command in self.commands_list_for_logged_in_user:
            return self.forbidden_command_for_not_logged_in_user()
        elif command == "register":
            return self.handling_register_command(data)
        elif command == "login":
            return self.handling_login_command(data)

    def handling_commands_for_logged_in_user(self, command):
        if command not in self.commands_list_for_logged_in_user and command in self.commands_list_for_not_logged_in_user:
            return self.forbidden_command_for_logged_in_user()
        elif command == "uptime":
            return self.uptime()
        elif command == "info":
            return self.info()
        elif command == "logout":
            return self.handling_logout_command()

    def response_to_client(self, client_request):
        command, data = client_request[0], client_request[1]
        if command == "stop":
            return self.stop_command()
        elif command == "help":
            return self.help()
        elif command not in self.all_commands_list:
            return self.unknown_command(command)
        if self.user_logging_status:
            return self.handling_commands_for_logged_in_user(command)
        else:
            return self.handling_commands_for_not_logged_in_user(command, data)

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






