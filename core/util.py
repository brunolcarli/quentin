"""
Utilitaries and tools.
"""
from base64 import b64encode, b64decode
import json
import requests

class FileTransformer:
    """
    Process file encoding/decoding to insert on database
    """
    @staticmethod
    def encode(content):
        """
        Prepare data for storage.
        """
        return json.dumps(b64encode(content).decode('utf-8'))

    @staticmethod
    def decode(content):
        """
        Prepare data retrieved from database to be delivered.
        """
        return b64decode(content)

    @staticmethod
    def get_file_data(path):
        """
        Opens a file from disk to return its bytes representation.
        """
        with open(path, 'rb') as file:
            file_data = file.read()
        return file_data

    @staticmethod
    def get_file_from_url(url):
        """
        Get bytes representation from discord media by its URL.
        """
        return requests.get(url).content


def paginate(data, slice_size=5):
    """
    Chunks an list to paginate it.
    Default pagination size is 5.
    return: list of lists
    """
    for i in range(0, len(data), slice_size):
        yield data[i:i + slice_size]

