import requests
import settings

def get_shortenURL(long_url):
    url = 'https://api-ssl.bitly.com/v3/shorten'
    
    query = {
            'access_token': settings.BITLY_TOKEN,
            'longurl':long_url
            }
    r = requests.get(url,params=query).json()['data']['url']
    return r