from data_utils import serialize_json, deserialize_json
from models import User


def request_to_server(user):
    if user.logged_in == True:
        request = input("Choose command: uptime / info / help / show / change data / logout / stop \n")
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
    elif client_request == "show":
        user = kwargs.get("user")
        return user.show_current_data()
    elif client_request == "login":
        user = kwargs.get("user")
        login_data = kwargs.get("login_data")
        login_data_dict = deserialize_json(login_data)
        return user.login_user(login_data_dict)
    elif client_request == "change data":
        user = kwargs.get("user")
        new_data = kwargs.get("new_data")
        new_data_dict = deserialize_json(new_data)
        return user.change_user_data(new_data_dict)
    elif client_request == "logout":
        return command.logout()
    else:
        error_msg = {
            "Unknown command": f"'{client_request}', try again"
        }
        return serialize_json(error_msg)




