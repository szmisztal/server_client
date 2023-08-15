import json
from variables import utf8

def serialize_json(data):
    return json.dumps(data).encode(utf8)

def deserialize_json(data):
    return json.loads(data)
