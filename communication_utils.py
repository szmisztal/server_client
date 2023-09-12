from data_utils import serialize_json, deserialize_json
from models import User

def request_to_server(user):
    if user.logged_in == True:
        request = input("--------------------------------------------------------\n"
                        "Choose command: uptime / info / help / show data / change data / send message / "
                        "inbox / archived messages / logout / stop \n"
                        "--------------------------------------------------------\n"
                        "REQUEST: ")
        return request
    else:
        request = input("--------------------------------------------------------\n"
                        "Choose command: register / login / stop \n"
                        "--------------------------------------------------------\n"
                        "REQUEST: ")
        return request

def read_server_response(data_dict):
    for key, value in data_dict.items():
        print(f">>>>> {key}: {value}")

def response_to_client(client_request, **kwargs):
    command = kwargs.get("command")
    user = kwargs.get("user")
    if client_request == "uptime":
        server_start_time = kwargs.get("server_start_time")
        return command.uptime(server_start_time)
    elif client_request == "info":
        return command.info()
    elif client_request == "help":
        return command.help()
    elif client_request in ["admin register", "register"]:
        registration_data = kwargs.get("registration_data")
        registration_data_dict = deserialize_json(registration_data)
        return User.register_user(registration_data_dict)
    elif client_request == "show data":
        return user.show_current_data()
    elif client_request  == "login":
        login_data = kwargs.get("login_data")
        login_data_dict = deserialize_json(login_data)
        return user.login_user(login_data_dict)
    elif client_request == "change data":
        new_data = kwargs.get("new_data")
        new_data_dict = deserialize_json(new_data)
        return user.change_user_data(new_data_dict)
    elif client_request == "send message":
        recipient_data = kwargs.get("recipient_data")
        message_data = kwargs.get("message_data")
        if recipient_data and message_data:
            recipient_data = deserialize_json(recipient_data)
            message_data = deserialize_json(message_data)
            return user.send_message(recipient_data, message_data)
        elif recipient_data:
            recipient_data = deserialize_json(recipient_data)
            return serialize_json(recipient_data)
    elif client_request == "inbox":
        return user.show_new_messages()
    elif client_request == "archived messages":
        return user.show_archived_messages()
    elif client_request == "logout":
        return command.logout()
    else:
        error_msg = {
            "Unknown command": f"'{client_request}', try again"
        }
        return serialize_json(error_msg)



