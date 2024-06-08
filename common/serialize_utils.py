import json
from common.config_variables import encode_format


class SerializeUtils:
    """
    A utility class for serializing and deserializing data to and from JSON format.

    Attributes:
    ----------
    encode_format : str
        The format used for encoding strings.
    """

    def __init__(self):
        """
        Initializes the SerializeUtils with the specified encoding format.
        """
        self.encode_format = encode_format

    def serialize_to_json(self, dict_data):
        """
        Serializes a dictionary to a JSON formatted string and encodes it.

        Parameters:
        ----------
        dict_data : dict
            The dictionary to serialize.

        Returns:
        -------
        bytes
            The JSON formatted string encoded in the specified format.
        """
        return json.dumps(dict_data).encode(self.encode_format)

    def deserialize_json(self, dict_data):
        """
        Deserializes a JSON formatted string to a dictionary.

        Parameters:
        ----------
        dict_data : bytes
            The JSON formatted string to deserialize.

        Returns:
        -------
        dict
            The deserialized dictionary.
        """
        return json.loads(dict_data)

