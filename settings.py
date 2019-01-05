import shelve

with shelve.open("API_KEYS") as token:
    # CK = token["TWITTER_CONSUMER_KEY"]
    # CS = token["TWITTER_CONSUMER_SECRET"]
    # AT = token["TWITTER_ACCESS_TOKEN"]
    # ATS = token["TWITTER_ACCESS_TOKEN_SECRET"]

    DISCORD_TOKEN = token["DISCORD_TOKEN"]

    BITLY_TOKEN = token["BITLY_KEY"]

    TRANSLATE_URL = token["GAS_TRANS_URL"]

    # RIOT_TOKEN = token["RIOT_TOKEN"]