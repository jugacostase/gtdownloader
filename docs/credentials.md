## Twitter keys
To set up your twitter keys file you need to have a developer  account with access to the full-archive 
search. If you plan to use this as part of academic research, you can apply for researcher
access to the API at [Twitter Academic Research access.](https://developer.twitter.com/en/products/twitter-api/academic-research/application-info)

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

Once you have done that, you can initialize your TweetDownloader class by passing the twitter_keys.yaml as a parameter in the cnstructor:

```python
from gtdownloader import TweetDownloader

gtd = TweetDownloader(credentials='twitter_keys.yaml')
```