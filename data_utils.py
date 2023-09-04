import json
from variables import encode_format

def serialize_to_json(data):
    return json.dumps(data).encode(encode_format)

def deserialize_json(data):
    return json.loads(data)



