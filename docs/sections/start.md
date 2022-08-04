# GTdownloader

GTdownloader is a geographical tweets downloading tool that leverages the [Twitter API](https://developer.twitter.com/en/docs/twitter-api) 
and [searchtweets-v2](https://pypi.org/project/searchtweets-v2/) to retrieve tweets with geographical information and store them in easy access 
formats like .csv and .shp.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install gtdownloader.

```bash
pip install gtdownloader
```

## Twitter keys
To set up your twitter keys file you need to have a developer  account with access to the full-archive 
search. If you plan to use this as part of academic research, you can apply for researcher
access to the API at [Twitter Academic Research access.](https://developer.twitter.com/en/products/twitter-api/academic-research/application-info)

After loging into your developer account, copy the consumer key, the consumer secret and the bearer token into a .yaml
file in the following way:

```yaml
search_tweets_v2:
  endpoint:  https://api.twitter.com/2/tweets/search/all
  consumer_key: YOUR_CONSUMER_KEY
  consumer_secret: YOUR_CONSUMER_SECRET
  bearer_token:  YOUR_BEARER_TOKEN
```

## Downloading tweets
Create a TweetDownloader object by passing the path with the credentials .yaml as a parameter
```python
from gtdownloader import TweetDownloader

# create downloader using Twitter API credentials
gtd = TweetDownloader(credentials='twitter_keys.yaml')
```
Use the .get_tweets() function to retrieve tweets containing the words you need within a specific date range. See all available search parameters at get_tweets()
```python
# get a batch of 10 tweets in english containing the word "tornado"
# between the dates 07/23/2022 and 07/29/2022
gtd.get_tweets('tornado', 
               lang='en', 
               max_tweets=10,
               start_time='07/23/2022', 
               end_time='07/29/2022'
               )

# accessing tweets data frame
gtd.tweets_df.head()
```

|    | text                                                                                                                                                                                                                                                                                                      |     conversation_id | created_at               | geo                              |                  id | public_metrics                                                              |           author_id | place_id         | date                      |   likes |   replies |   retweets |
|---:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------:|:-------------------------|:---------------------------------|--------------------:|:----------------------------------------------------------------------------|--------------------:|:-----------------|:--------------------------|--------:|----------:|-----------:|
|  0 | @nexton9news We heard sirens around our neighborhood. Was a police search for a shooter.But no alert.We found out from our nextdoor app initially. There has to be a better way to protect our community! You wont get sucked into a tornado but you just might get shot! Really? https://t.co/egK4DGZB04 | 1552802683655819264 | 2022-07-28T23:46:24.000Z | {'place_id': '07d9c9ffed484001'} | 1552802683655819264 | {'retweet_count': 0, 'reply_count': 1, 'like_count': 0, 'quote_count': 0}   | 1552785506060029952 | 07d9c9ffed484001 | 2022-07-28 23:46:24+00:00 |       0 |         1 |          0 |
|  1 | At 10:47 AM EDT, 3 NNE Bliss [Wyoming Co, NY] NWS STORM SURVEY reports TORNADO. CORRECTS PREVIOUS TORNADO REPORT FOR UPDATED PATH WIDTH FROM 3 NNE BLISS. CORRECTS PREVIOUS TORNADO REPORT FROM 3 NNE BLISS. PRELIMINARY STORM SURVEY OF EF-2 TORNADO... https://t.co/zeuOeWgU1h                          | 1552798558377496577 | 2022-07-28T23:30:00.000Z | {'place_id': '94965b2c45386f87'} | 1552798558377496577 | {'retweet_count': 1, 'reply_count': 0, 'like_count': 2, 'quote_count': 0}   |            34921066 | 94965b2c45386f87 | 2022-07-28 23:30:00+00:00 |       2 |         0 |          1 |
|  2 | Kent Ct. Fire Dept.  Going out for a possible tornado touchdown.                                                                                                                                                                                                                                          | 1552793684265025536 | 2022-07-28T23:10:38.000Z | {'place_id': '00b644805cf59d2c'} | 1552793684265025536 | {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0}   |  807683560861794304 | 00b644805cf59d2c | 2022-07-28 23:10:38+00:00 |       0 |         0 |          0 |
|  3 | Tornado possible with this Ma Warning ⚠️ severe storm. Tornado Tagged. 🌪 https://t.co/p6zPotKz1Y                                                                                                                                                                                                           | 1552792408101978113 | 2022-07-28T23:05:34.000Z | {'place_id': 'cd450c94084cbf9b'} | 1552792408101978113 | {'retweet_count': 1, 'reply_count': 1, 'like_count': 0, 'quote_count': 0}   |          2382930566 | cd450c94084cbf9b | 2022-07-28 23:05:34+00:00 |       0 |         1 |          1 |
|  4 | #STORM12ALERT Severe Thunderstorm Warning for Cumberland, Van Buren, Warren and White County in TN until 6:15pm. #TNWX TORNADO POSSIBLE https://t.co/AqTpkt0oL5                                                                                                                                           | 1552790806553042944 | 2022-07-28T22:59:12.000Z | {'place_id': '0013b7ea2894e530'} | 1552790806553042944 | {'retweet_count': 0, 'reply_count': 0, 'like_count': 1, 'quote_count': 0}   | 1217238095977906176 | 0013b7ea2894e530 | 2022-07-28 22:59:12+00:00 |       1 |         0 |          0 |
|  5 | Tornado possible with this warned ⚠️  storm over N.H. ! Tornado tagged. https://t.co/dbyt08Y5F2                                                                                                                                                                                                            | 1552789697306533888 | 2022-07-28T22:54:47.000Z | {'place_id': 'cd450c94084cbf9b'} | 1552789697306533888 | {'retweet_count': 0, 'reply_count': 0, 'like_count': 1, 'quote_count': 0}   |          2382930566 | cd450c94084cbf9b | 2022-07-28 22:54:47+00:00 |       1 |         0 |          0 |
|  6 | After an EF-2 tornado touched down in Wyoming county earlier this morning it’s remarkable no human or animal was injured, or killed in its path. https://t.co/seB20KVgYd                                                                                                                                  | 1552788408283668481 | 2022-07-28T22:49:40.000Z | {'place_id': '94965b2c45386f87'} | 1552788408283668481 | {'retweet_count': 1, 'reply_count': 1, 'like_count': 11, 'quote_count': 0}  |  914664091867807744 | 94965b2c45386f87 | 2022-07-28 22:49:40+00:00 |      11 |         1 |          1 |
|  7 | Tornado Warning continues for Spencer TN until 6:00 PM CDT https://t.co/qi5F89XbsS                                                                                                                                                                                                                        | 1552787583494541312 | 2022-07-28T22:46:23.000Z | {'place_id': '7f7d58e5229c6b6c'} | 1552787583494541312 | {'retweet_count': 6, 'reply_count': 0, 'like_count': 12, 'quote_count': 0}  |           596841936 | 7f7d58e5229c6b6c | 2022-07-28 22:46:23+00:00 |      12 |         0 |          6 |
|  8 | Tornado Warning continues for Spencer TN until 6:00 PM CDT https://t.co/HjVvvixX2A                                                                                                                                                                                                                        | 1552787570395729920 | 2022-07-28T22:46:20.000Z | {'place_id': '7f7d58e5229c6b6c'} | 1552787570395729920 | {'retweet_count': 19, 'reply_count': 4, 'like_count': 47, 'quote_count': 1} |          2544227706 | 7f7d58e5229c6b6c | 2022-07-28 22:46:20+00:00 |      47 |         4 |         19 |
|  9 | I know today has been a hard day for Kentucky. But there is hope after natural disasters.                                                                                                                                                                                                                 | 1552786945746550784 | 2022-07-28T22:43:51.000Z | {'place_id': 'ca0d320dd40f586b'} | 1552786945746550784 | {'retweet_count': 5, 'reply_count': 0, 'like_count': 9, 'quote_count': 0}   |          2488543704 | ca0d320dd40f586b | 2022-07-28 22:43:51+00:00 |       9 |         0 |          5 |

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)