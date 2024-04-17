from server_side.server_messages import MessageTemplate


class ClientRequests:
    def __init__(self):
        self.message_template = MessageTemplate("REQUEST")

    def user_data_input(self):
        username = input("Username: ")
        password = input("Password: ")
        user_data = {
            "username": username,
            "password": password
        }
        return user_data

    def user_data_handling(self, command):
        user_data = self.user_data_input()
        return self.message_template.template(message = command, data = user_data)

    def request_to_server(self):
        command = input("REQUEST: ").lower()
        if command in ["register", "login"]:
            return self.user_data_handling(command)
        return self.message_template.template(message = command)
