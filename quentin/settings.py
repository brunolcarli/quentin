"""
Common shared system settings.
"""
import os


__version__ = '0.0.1.'

# General configs
ENV_REF = os.environ.get('ENV_REF', 'development')

# Bot configs
TOKEN = os.environ.get('TOKEN')

# The Movie Database API configs
TMDB_API = 'https://api.themoviedb.org/3/'
TMDB_KEY = {'api_key': os.getenv('TMDB_KEY')}
IMG_URL = 'https://image.tmdb.org/t/p/w500/'


# Redis (cache)
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

# Mysql (database)
MYSQL_CONFIG = {
    'MYSQL_HOST': os.environ.get('MYSQL_HOST'),
    'MYSQL_USER': os.environ.get('MYSQL_USER'),
    'MYSQL_PASSWORD': os.environ.get('MYSQL_PASSWORD'),
    'MYSQL_DATABASE': os.environ.get('MYSQL_DATABASE'),
    'MYSQL_ROOT_PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD')
}
