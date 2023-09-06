from data_utils import DataUtils


class UserUtils:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged_in = False
        self.data_utils = DataUtils()
        self.users_file = "users_list.json"
        self.users_list = self.data_utils.read_json_file(self.users_file) or []

    def validate_username(self, username):
        for u in self.users_list:
            stored_username = u["username"]
            if stored_username == username:
                return False
        return True

    def validate_username_and_password(self, username, password):
        for u in self.users_list:
            stored_username = u["username"]
            stored_password = u["password"]
            if stored_username == username and stored_password == password:
                return True
        return False

    def add_user_to_list_and_write_to_file(self, user_data):
        self.users_list.append(user_data)
        self.data_utils.write_to_json_file(self.users_file, self.users_list) or []

    def register_user(self, client_request):
        user_data = client_request["User"]
        username = user_data["username"]
        validated_username = self.validate_username(username)
        if validated_username == True:
            self.add_user_to_list_and_write_to_file(user_data)
            register_message = {
                f"User '{username}'": "Registered successfully"
            }
            return register_message
        else:
            error_message = {
                "Username": "In use, choose another"
            }
            return error_message

    def login_user(self, client_request):
        user_data = client_request["User"]
        username = user_data["username"]
        password = user_data["password"]
        validated_data = self.validate_username_and_password(username, password)
        if validated_data == True:
            user = UserUtils(username, password)
            user.logged_in = True
            login_message = {
                f"User '{user.username}'": "Log in successfully"
            }
            return login_message
        else:
            error_message = {
                "Incorrect data": "Try again"
            }
            return error_message
#
#     def login_user(self, login_data_dict):
#         self.username = login_data_dict["username"]
#         self.password = login_data_dict["password"]
#         self.admin_role = login_data_dict["admin_role"]
#         for u in users_list:
#             stored_username = u["username"]
#             stored_password = u["password"]
#             if self.username == stored_username and self.password == stored_password:
#                 if self.admin_role == True:
#                     login_msg = {
#                         "Admin": "You`re welcome"
#                     }
#                 else:
#                     login_msg = {
#                         "Message": "You was logged in"
#                     }
#                 return serialize_json(login_msg)
#         error_msg = {
#             "Message": "Incorrect data. try again"
#         }
#         return serialize_json(error_msg)
#
#     def is_logged_in(self):
#         return self.logged_in
#
#     def show_current_data(self):
#         current_data_msg = {
#             "Your current username and password:": f"Username: {self.username}, password: {self.password}, admin role: {self.admin_role}"
#         }
#         return serialize_json(current_data_msg)
#
#     def change_user_data(self, new_data_dict):
#         new_username = new_data_dict["username"]
#         new_password = new_data_dict["password"]
#         new_messages = read_json_file(f"{self.username}_new_messages.json") or []
#         archived_messages = read_json_file(f"{self.username}_archived_messages.json") or []
#         for u in users_list:
#             stored_username = u["username"]
#             if stored_username == new_username and stored_username != self.username:
#                 error_msg = {
#                     "Username": "In use, choose another"
#                 }
#                 return serialize_json(error_msg)
#         for u in users_list:
#             if self.username == u["username"]:
#                 u["username"] = self.username = new_username
#                 u["password"] = self.password = new_password
#                 write_to_json_file(users_file, users_list)
#                 write_to_json_file(f"{self.username}_new_messages.json", new_messages)
#                 write_to_json_file(f"{self.username}_archived_messages.json", archived_messages)
#                 success_msg = {
#                     "Success": f"Your new data: username = {self.username}, password = {self.password}"
#                 }
#                 return serialize_json(success_msg)
#
#     def send_message(self,  recipient_data, message_data):
#         message = message_data["message"]
#         recipient = recipient_data["username"]
#         recipient_messages = read_json_file(f"{recipient}_new_messages.json") or []
#         if len(message) > 255:
#             error_msg = {
#                 "Message": "Failed, max message length = 255"
#             }
#             return serialize_json(error_msg)
#         elif len(recipient_messages) >= 5:
#             if self.admin_role == False:
#                 error_msg = {
#                     "Message": "Failed, inbox full"
#                 }
#                 return serialize_json(error_msg)
#             else:
#                 pass
#         else:
#             message_dict = {
#                 "Message from": self.username,
#                 "Text": message
#             }
#             recipient_messages.append(message_dict)
#             write_to_json_file(f"{recipient}_new_messages.json", recipient_messages)
#             success_msg = {
#                 "Message": "Message send successfully"
#             }
#             return serialize_json(success_msg)
#
#     def show_new_messages(self):
#         new_messages = read_json_file(f"{self.username}_new_messages.json") or []
#         messages_to_read = new_messages.copy()
#         archived_messages = read_json_file(f"{self.username}_archived_messages.json")
#         archived_messages.extend(new_messages)
#         new_messages = []
#         write_to_json_file(f"{self.username}_new_messages.json", new_messages)
#         write_to_json_file(f"{self.username}_archived_messages.json", archived_messages)
#         return serialize_json(messages_to_read)
#
#     def show_archived_messages(self):
#         archived_messages = read_json_file(f"{self.username}_archived_messages.json")
#         return serialize_json(archived_messages)
#
#     def __str__(self):
#         return f"{self.username}, {self.password}, {self.logged_in}, {self.admin_role}"
#
#
# # INPUT FUNCTIONS
# def recipient_input():
#     recipient = input("Who do you want to send a message to ?: ")
#     for u in users_list:
#         if recipient == u["username"]:
#             recipient_data = {
#                 "username": u["username"]
#             }
#             return recipient_data
#     else:
#         error_msg ={
#             "Error": "User not found"
#         }
#         return error_msg
#
# def message_input():
#     message = input("Write a message: ")
#     message_data = {
#         "message": message
#     }
#     return message_data
