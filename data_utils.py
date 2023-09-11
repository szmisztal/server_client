import json


def serialize_json(data):
    return json.dumps(data)

def deserialize_json(data):
    return json.loads(data)

def write_to_json_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent = 4)

def read_json_file(filename):
    try:
        with open(filename, "r") as file:
            users_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users_data = []
    return users_data


