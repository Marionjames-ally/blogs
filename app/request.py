import urllib.request,json
from .user import User

# Getting api key
api_key = None

# Getting the movie base url
base_url = None

def configure_request(app):
    global api_key,base_url
    api_key = app.config['QUOTE_API_KEY']
    base_url = app.config['QUOTE_API_BASE_URL'] 