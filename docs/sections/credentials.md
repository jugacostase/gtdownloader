## Twitter keys
To set up your twitter keys file you need to have a developer  account with access to the full-archive 
search. If you plan to use this as part of academic research, you can apply for researcher
access to the API at [Twitter Academic Research access.](https://developer.twitter.com/en/products/twitter-api/academic-research/application-info)

### YAML 

After loging into your developer account, open any text editor and copy the consumer key, the consumer secret and the bearer token into a .yaml
file in the following way:

```yaml
search_tweets_v2:
  endpoint:  https://api.twitter.com/2/tweets/search/all
  consumer_key: YOUR_CONSUMER_KEY
  consumer_secret: YOUR_CONSUMER_SECRET
  bearer_token:  YOUR_BEARER_TOKEN
```
Here we saved the file as "twitter_keys.yaml". 

Once you have done that, you can initialize your TweetDownloader class by passing the twitter_keys.yaml as a parameter in the constructor:

```python
from gtdownloader import TweetDownloader

gtd = TweetDownloader(yaml_credentials='twitter_keys.yaml')
```

### Environment variable

Instead of setting up a YAML file with credentials, you can also set your Twitter API bearer token as an environment variable and pass it to the TweetDownloader initializer:

```python
from gtdownloader import TweetDownloader

gtd = TweetDownloader(env_token='TWITTER_KEY_ENV_VAR')
```

### Bearer token

Even though it is not recommended, you can also pass the bearer token directly to the initializer:

```python
from gtdownloader import TweetDownloader

gtd = TweetDownloader(bearer_token='TWITTER_BEARER_TOKEN')
```