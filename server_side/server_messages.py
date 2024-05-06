from datetime import datetime as dt
from users_utils import User
from common.message_template import MessageTemplate


class ServerResponses:
    def __init__(self):
        self.message_template = MessageTemplate("RESPONSE")

    def welcome_message(self):
        return self.message_template.template(message = "Type 'help' to see available commands")

    def server_uptime_command(self, server_uptime):
        return self.message_template.template(message = f"Server uptime - {server_uptime}")

    def info_command(self, server_info):
        return self.message_template.template(message = "Server info: ", data = server_info)

    def help_command(self, commands_list):
        return self.message_template.template(message = "Available commands: ", data = commands_list)

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

    def username_in_use_message(self):
        return self.message_template.template(message = "Username in use, choose another one")

    def user_sign_in_successfully(self):
        return self.message_template.template(message = "You are logged in successfully")

    def wrong_credentials(self):
        return self.message_template.template(message = "Wrong username or password, try again")

    def change_data_successfully(self):
        return self.message_template.template(message = "Data changed successfully")

    def negative_decision_for_delete_account(self):
        return self.message_template.template(message = "You account stay in database")

    def delete_account_successfully(self):
        return self.message_template.template(message = "You were successfully delete from database")

    def recipient_not_found(self):
        return self.message_template.template(message = "Recipient not found, try again")

    def mail_error(self):
        return self.message_template.template(message = "Message is too long or recipient mailbox is full")

    def mail_send_successfully(self):
        return self.message_template.template(message = "Mail send successfully")

    def empty_mailbox(self):
        return self.message_template.template(message = "Your mailbox is empty")

    def messages_in_mailbox(self, messages_list):
        return self.message_template.template(message = "Messages: ", data = messages_list)


class HandlingClientCommands:
    def __init__(self, server):
        self.server = server
        self.response = ServerResponses()
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

    def uptime(self):
        current_time = dt.now()
        server_uptime = current_time - self.server.server_start_time
        return self.response.server_uptime_command(server_uptime)

    def info(self):
        server_info = {
            "Server start date:": self.server.server_start_date,
            "Server version:": self.server.server_version
        }
        return self.response.info_command(server_info)

    def help(self):
        if self.user_logging_status:
            commands = {
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
            commands = {
                "Help": "Shows available commands",
                "Register": "Sign up new user",
                "Login": "Sign in the user",
                "Stop": "Shuts down the server"
            }
        return self.response.help_command(commands)

    def handling_register_command(self, user_data):
        verify_username = self.user.register_user(user_data)
        if verify_username is True:
            return self.response.user_register_successfully()
        return self.response.username_in_use_message()

    def handling_login_command(self, user_data):
        verify_credentials = self.user.login_user(user_data)
        if verify_credentials:
            self.user_username = user_data["username"]
            self.user_logging_status = True
            return self.response.user_sign_in_successfully()
        return self.response.wrong_credentials()

    def handling_logout_command(self):
        self.user_logging_status = False
        self.user_username = None
        return self.response.message_template.template(message = "You were log out successfully")

    def handling_change_data_command(self, user_data):
        verify_username = self.user.change_user_data(user_data)
        if verify_username is True:
            self.user_username = user_data["username"]
            return self.response.change_data_successfully()
        return self.response.username_in_use_message()

    def handling_delete_account_command(self, data):
        verify_decision = self.user.delete_user(data)
        if verify_decision:
            self.user_username = None
            self.user_logging_status = False
            return self.response.delete_account_successfully()
        return self.response.negative_decision_for_delete_account()

    def handling_send_message_command(self, data):
        verify_recipient_and_message = self.user.send_message(data)
        if verify_recipient_and_message is None:
            return self.response.recipient_not_found()
        elif verify_recipient_and_message is False:
            return self.response.mail_error()
        else:
            return self.response.mail_send_successfully()

    def handling_mailbox_command(self, unread_mails_condition):
        if unread_mails_condition is True:
            messages_list = self.user.show_archived_messages()
        else:
            messages_list = self.user.show_unread_messages()
        if messages_list is []:
            return self.response.empty_mailbox()
        return self.response.messages_in_mailbox(messages_list)

    def handling_commands_for_not_logged_in_user(self, command, data):
        if command not in self.commands_list_for_not_logged_in_user and command in self.commands_list_for_logged_in_user:
            return self.response.forbidden_command_for_not_logged_in_user()
        elif command == "register":
            return self.handling_register_command(data)
        elif command == "login":
            return self.handling_login_command(data)

    def handling_commands_for_logged_in_user(self, command, data):
        if command not in self.commands_list_for_logged_in_user and command in self.commands_list_for_not_logged_in_user:
            return self.response.forbidden_command_for_logged_in_user()
        elif command == "uptime":
            return self.uptime()
        elif command == "info":
            return self.info()
        elif command == "logout":
            return self.handling_logout_command()
        elif command == "change data":
            return self.handling_change_data_command(data)
        elif command == "delete":
            return self.handling_delete_account_command(data)
        elif command == "send message":
            return self.handling_send_message_command(data)
        elif command == "mailbox":
            return self.handling_mailbox_command(False)
        elif command == "archives":
            return self.handling_mailbox_command(True)

    def response_to_client(self, client_request):
        command, data = client_request[0], client_request[1]
        if command == "stop":
            return self.response.stop_command()
        elif command == "help":
            return self.help()
        elif command not in self.all_commands_list:
            return self.response.unknown_command(command)
        if self.user_logging_status:
            return self.handling_commands_for_logged_in_user(command, data)
        else:
            return self.handling_commands_for_not_logged_in_user(command, data)







