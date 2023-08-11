server_info = "Server was created 11.08.2023, actual version: 1.0.0"

def server_response(client_request):
    if client_request == "uptime":
        print("1 hour")
    elif client_request == "info":
        print(server_info)
    elif client_request == "help":
        print(f"Commands: uptime - server life time \ninfo - server info \nhelp - commands list \nstop - server stop")

