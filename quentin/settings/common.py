"""
Common shared system settings.
"""
import os


__version__ = '0.0.0.'

# General configs
ENV_REF = os.environ.get('ENV_REF', 'development')

# Bot configs
TOKEN = os.environ.get('TOKEN')

# The Movie Database configss
TMDB_API = 'https://api.themoviedb.org/3/'
TMDB_KEY = {'api_key': os.getenv('TMDB_KEY')}
IMG_URL = 'https://image.tmdb.org/t/p/w500/'
