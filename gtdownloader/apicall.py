import os
import requests
from ._utils.utils import load_credentials

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields

KEYS = {}

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {KEYS['bearer_token']}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def retrieve_tweets(query_params, keys):
    search_url = "https://api.twitter.com/2/tweets/search/all"
    global KEYS

    print('ALL-ENVIRON', os.environ)

    try:
        KEYS = load_credentials(keys)
    except Exception as e:
        try:
            KEYS['bearer_token'] = os.environ[keys]
        except KeyError:
            KEYS['bearer_token'] = keys
    response = requests.request("GET", search_url, auth=bearer_oauth, params=query_params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


