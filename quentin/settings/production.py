from quentin.settings.common import *


MYSQL_CONFIG = {
    'MYSQL_HOST': os.environ.get('MYSQL_HOST'),
    'MYSQL_USER': os.environ.get('MYSQL_USER'),
    'MYSQL_PASSWORD': os.environ.get('MYSQL_PASSWORD'),
    'MYSQL_DATABASE': os.environ.get('MYSQL_DATABASE'),
    'MYSQL_ROOT_PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD')
}
