from data_utils import serialize_json
from variables import utf8

def request_to_server():
    request = input("Choose command: uptime / info / help / stop \n").encode(utf8)
    return request

def response_to_client(self, client_request, server_start_time):
    if client_request == "uptime":
        return self.uptime(server_start_time)
    elif client_request == "info":
        return self.info()
    elif client_request == "help":
        return self.help()
    else:
        error_msg = {
            "Unknown command": f"'{client_request}', try again"
        }
        return serialize_json(error_msg).encode(utf8)

