import json
from variables import utf8

def serialize_json(data):
    return json.dumps(data)

def deserialize_json(data):
    return json.loads(data)

def write_to_json_file(filename, data):
    with open(filename, "a") as file:
        json.dump(data, file, indent = 4)

def read_json_file(filename):
    with open(filename, "r") as file:
        json_object = json.load(file)
    return json_object

