import json


def serialize_json(data):
    return json.dumps(data)

def deserialize_json(data):
    return json.loads(data)

def write_to_json_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent = 4)

def read_json_file(filename):
    with open(filename, "r") as file:
        users_data = json.load(file)
    return users_data

def user_username_and_password_input():
    username = input("Username: ")
    password = input("Password: ")
    user_data = {
        "username": username,
        "password": password
    }
    return user_data
