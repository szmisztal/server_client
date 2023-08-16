import json
from variables import utf8

def serialize_json(data):
    return json.dumps(data).encode(utf8)

def deserialize_json(data):
    return json.loads(data)

def write_to_json_file(file, data):
    with open(file, "w") as file:
        json.dump(data, file)

def read_json_file(file):
    with open(file, "r") as file:
        json_object = json.load(file)
    return json_object
