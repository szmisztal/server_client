from data_utils import serialize_json, deserialize_json, read_json_file
from models import User
from variables import users_file


def request_to_server(user):
    print(user)
    if user.logged_in == True:
        request = input("Choose command: uptime / info / help / logout / stop \n")
        return request
    else:
        request = input("Choose command: register / login / stop \n")
        return request

def response_to_client(client_request, **kwargs):
    command = kwargs.get("command")
    if client_request == "uptime":
        server_start_time = kwargs.get("server_start_time")
        return command.uptime(server_start_time)
    elif client_request == "info":
        return command.info()
    elif client_request == "help":
        return command.help()
    elif client_request == "register":
        registration_data = kwargs.get("registration_data")
        registration_data_dict = deserialize_json(registration_data)
        return User.register_user(registration_data_dict)
    elif client_request == "login":
        login_data = kwargs.get("login_data")
        login_data_dict = deserialize_json(login_data)
        return login_user(login_data_dict)
    elif client_request == "logout":
        return command.logout()
    else:
        error_msg = {
            "Unknown command": f"'{client_request}', try again"
        }
        return serialize_json(error_msg)

def login_user(login_data_dict):
    username = login_data_dict["username"]
    password = login_data_dict["password"]
    users_list = read_json_file(users_file)
    for user_data in users_list:
        stored_username = user_data["username"]
        stored_password = user_data["password"]
        if username == stored_username and password == stored_password:
            login_msg = {
                "Message": "You was logged in"
            }
            return serialize_json(login_msg)
    error_msg = {
        "Message": "Incorrect data. try again"
    }
    return serialize_json(error_msg)


