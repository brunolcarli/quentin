import requests
from quentin.settings import TMDB_KEY, TMDB_API


def get_trending(media, time_ref, page):
    """
    Request trending media on a time ref (day or week)
    """
    url = f'{TMDB_API}/trending/{media}/{time_ref}?page={page}'
    payload = ""
    response = requests.request("GET", url, data=payload, params=TMDB_KEY)

    return response.json()
