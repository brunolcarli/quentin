import json
import mysql.connector
from core.db_handler import Database
from core.util import FileTransformer
from quentin.settings import MYSQL_CONFIG
from datetime import datetime


class TestDabaseFunctionality:
    """
    Test the database handler and operations.
    """
    # Setup
    connection = mysql.connector.connect(
        host=MYSQL_CONFIG['MYSQL_HOST'],
        user=MYSQL_CONFIG['MYSQL_USER'],
        password=MYSQL_CONFIG['MYSQL_PASSWORD'],
        database='test_db'
    )
    cursor = connection.cursor()
    db = Database('test_db')
    test_file_path = 'tests/lisa_by_beelzebruno.png'
    test_file = FileTransformer.encode(FileTransformer.get_file_data(test_file_path))

    # manually insert data for test retrieving
    cursor.execute(
        f'''
        INSERT INTO storage (id, user_id, file, url, extension)
        VALUES (666, 666, {test_file}, "foo", "baz");
        '''
    )
    connection.commit()

    def test_migration(self):
        """
        Test table creation.
        """
        self.cursor.execute('show tables;')

        # assert that the table exists after migration
        tables = self.cursor.fetchall()
        assert any([table for table in tables if table[0] == 'storage'])
        
    def test_insert_file(self):
        """
        Test insertion functionality.
        """
        # open test image
        item_id = self.db.insert(
            666, self.test_file, json.dumps('http://foo.baz/666/'), json.dumps('png')
        )

        # the item id is incremented from previous inserted item on setup
        assert item_id == 667

    def test_retrieve_file_by_id(self):
        """
        Test that a file can be retrieved from database by its ID.
        """
        # collect insert data
        results = self.db.select(666)
        id, user_id, dump, url, extension, date = results[0]

        assert id == 666
        assert user_id == 666
        assert FileTransformer.decode(dump) == FileTransformer.decode(self.test_file)
        assert url == 'foo'
        assert extension == 'baz'
        assert isinstance(date, datetime)
