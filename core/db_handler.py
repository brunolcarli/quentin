import mysql.connector
from quentin.settings import MYSQL_CONFIG


class Database:

    def __init__(self, database):
        self.connection = self.connect()
        self.cursor = self.connection.cursor()
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(
            host=MYSQL_CONFIG['MYSQL_HOST'],
            user=MYSQL_CONFIG['MYSQL_USER'],
            password=MYSQL_CONFIG['MYSQL_PASSWORD'],
            database=self.database
        )
        return connection

    def select(self, item_id):
        self.cursor.execute(
            f'''
            SELECT * FROM storage WHERE id={item_id};
            '''
        )
        return self.cursor.fetchall()

    def insert(self, user_id, file, url, ext):
        
        query =  f'''
            INSERT INTO storage (user_id, file, url, extension)
            VALUES ({user_id}, {file}, {url}, {ext});
            '''
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    def close(self):
        self.connection.close()


def migrate():
    """
    Creates initial database schema.
    """
    print('Migrating database...')
    connection = mysql.connector.connect(
        host=MYSQL_CONFIG['MYSQL_HOST'],
        user=MYSQL_CONFIG['MYSQL_USER'],
        password=MYSQL_CONFIG['MYSQL_PASSWORD'],
    )
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE DATABASE quentin;')
    except mysql.connector.errors.DatabaseError:
        pass
    cursor.execute('USE quentin;')
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS storage (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT,
            file LONGTEXT,
            url TEXT,
            extension VARCHAR(3),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
    )
    connection.close()
    print('Migration completed!')
