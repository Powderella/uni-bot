import requests
import settings

def translate(text, source, target):
    target_url = settings.TRANSLATE_URL
    params = {"text":text, "source":source, "target":target}

    req = requests.get(target_url, params = params)
    return req.text