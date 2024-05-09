import json
from common.config_variables import encode_format


class SerializeUtils:
    def __init__(self):
        self.encode_format = encode_format

    def serialize_to_json(self, dict_data):
        return json.dumps(dict_data).encode(self.encode_format)

    def deserialize_json(self, dict_data):
        return json.loads(dict_data)
