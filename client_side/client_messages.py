from server_side.server_messages import MessageTemplate


class ClientRequests:
    def __init__(self):
        self.message_template = MessageTemplate("REQUEST")

    def user_data_input(self):
        username = input("(New) Username: ")
        password = input("(New) Password: ")
        user_data = {
            "username": username,
            "password": password
        }
        return user_data

    def user_data_handling(self, command):
        user_data = self.user_data_input()
        return self.message_template.template(message = command, data = user_data)

    def delete_account_confirmation_input(self):
        decision = input("Do you really want to delete your account ? Y/N").lower()
        return self.message_template.template(message = "delete", data = decision)

    def request_to_server(self):
        command = input("REQUEST: ").lower()
        if command in ["register", "login", "change data"]:
            return self.user_data_handling(command)
        elif command == "delete":
            return self.delete_account_confirmation_input()
        return self.message_template.template(message = command)
