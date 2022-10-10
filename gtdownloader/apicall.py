import requests
from ._utils.utils import load_credentials

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev',
                'tweet.fields': 'author_id'}


KEYS = load_credentials('credentials/twitter_keys.yaml')

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {KEYS['bearer_token']}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def retrieve_tweets(query_params):
    search_url = "https://api.twitter.com/2/tweets/search/all"
    response = requests.request("GET", search_url, auth=bearer_oauth, params=query_params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


