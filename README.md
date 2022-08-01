# GTdownloader

GTdownloader is a geographical tweets downloading tool that leverages the 
[Twitter API](https://developer.twitter.com/en/docs/twitter-api) and 
[searchtweets-v2](https://pypi.org/project/searchtweets-v2/) 
to retrieve tweets with geographical information and store them in easy access formats
like .csv and .shp.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install gtdownloader.

```bash
pip install gtdownloader
```

## Twitter keys
To set up your twitter keys file you need to have a developer  account with access to the full-archive 
search. If you plan to use this as part of academic research, you can apply for researcher
access to the API at 
[Twitter Academic Research access.](https://developer.twitter.com/en/products/twitter-api/academic-research/application-info)

After loging into your developer account, copy the consumer key, the consumer secret and the bearer token into a .yaml
file in the following way:

```yaml
search_tweets_v2:
  endpoint:  https://api.twitter.com/2/tweets/search/all
  consumer_key: YOUR_CONSUMER_KEY
  consumer_secret: YOUR_CONSUMER_SECRET
  bearer_token:  YOUR_BEARER_TOKEN
```

## Get started

```python
from gtdownloader import TweetDownloader

# create downloader using Twitter API credentials
gtd = TweetDownloader(credentials='twitter_keys.yaml')

# get a batch of 400 tweets in english containing the word "tornado"
# between the dates 07/23/2022 and 07/29/2022
gtd.get_tweets('tornado', 
               lang='en', 
               max_tweets=400,
               start_time='07/23/2022', 
               end_time='07/29/2022'
               )

# accessing tweets data frame
print(gtd.tweets_df.head())
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)