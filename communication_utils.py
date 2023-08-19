from data_utils import serialize_json, deserialize_json
from models import User


def request_to_server():
    request = input("Choose command: register / uptime / info / help / stop \n")
    return request

def response_to_client(client_request, **kwargs):
    command = kwargs.get("command")
    if command:
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
    else:
        error_msg = {
            "Unknown command": f"'{client_request}', try again"
        }
        return serialize_json(error_msg)




