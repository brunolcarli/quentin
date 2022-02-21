
from core.util import FileTransformer


class TestFileTransformer:
    """
    Tests related to file conversion for databse insertion and retrieving.
    """
    # Setup
    test_file_path = 'tests/lisa_by_beelzebruno.png'
    test_file_url = 'https://media.discordapp.net/attachments/590678517407285251/944755154907979776/lisa.png?width=750&height=422'

    def test_get_from_disk(self):
        """
        Test that FileTransformer opens file from disk.
        """
        file_data = FileTransformer.get_file_data(self.test_file_path)
        assert type(file_data) == bytes

    def test_get_from_url(self):
        """
        Test that FileTransformer opens file url.
        """
        file_data = FileTransformer.get_file_from_url(self.test_file_url)
        assert type(file_data) == bytes


    def test_encode_from_disk(self):
        """
        Test that FileTransformer encodes file from disk.
        """
        file_data = FileTransformer.get_file_data(self.test_file_path)
        dump = FileTransformer.encode(file_data)
        assert type(dump) == str

    def test_encode_from_url(self):
        """
        Test that FileTransformer encodes file url.
        """
        file_data = FileTransformer.get_file_from_url(self.test_file_url)
        dump = FileTransformer.encode(file_data)
        assert type(dump) == str

    def test_decode_from_disk(self):
        """
        Test that FileTransformer encodes decods a dumped file from disk.
        """
        # encoding
        file_data = FileTransformer.get_file_data(self.test_file_path)
        dump = FileTransformer.encode(file_data)

        # decoding
        decoded = FileTransformer.decode(dump)
        assert file_data == decoded

    def test_decode_from_url(self):
        """
        Test that FileTransformer decodes a dumped file url.
        """
        # encoding
        file_data = FileTransformer.get_file_from_url(self.test_file_url)
        dump = FileTransformer.encode(file_data)

        # decoding
        decoded = FileTransformer.decode(dump)
        assert file_data == decoded
