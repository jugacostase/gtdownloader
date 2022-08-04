# Downloading
The TweetDownloader object allows you to download and store tweets for further post-processing and exporting.

## Overview

There are three main functions used to download tweets:

| Function              | Description                                                                                |
|-----------------------|--------------------------------------------------------------------------------------------|
| [`get_tweets`]()      | Gets tweets from the Twitter API and user defined queries.                                 |
| [`get_replies`]()     | Gets replies on conversations originated from already downloaded tweets.                   |
| [`tweets_from_csv`]() | Gets tweets from the Twitter API and user defined queries using a csv file table as input. |

## Get tweets

To download tweets you need to initialize the TweetDownloader class by passing the credentials YAML file as a parameter in the class constructor. You can also name your project so all exported files have this string leading in their name. 
Additionally, you can specify the path to folder in which you want to save future results. 
```python
from gtdownloader import TweetDownloader

# create downloader using Twitter API credentials
gtd = TweetDownloader(name='Tennis_players_project', credentials='twitter_keys.yaml', output_folder='Tennis_project_downloads')
```

Once the function is initialized, you can call the get_tweets() method by passing a string you want to look up in Twitter and any additional parameter you want. Here we specify a language and a date range defined by start_time and end_time.
Here we want to see what people were saying about Rafael Nadal during the 6th and 7th of July of 2022, right after he beated Taylor Fritz at Wimbledon. Notice we set a maximum amount of downloaded tweets of 1000, although there is no guarantee that amount is going to be reached.

```python
gtd.get_tweets(
               query='(Nadal) OR (Rafael Nadal)',
               lang='en',
               start_time='07/06/2022',
               end_time='07/07/2022',
               max_tweets=1000            
)
```
The download will initiate by going through the Twitter API pagination with a next-page-token system. Given that Twitter API has monthly caps on the amount of tweets to download, a temp_ csv with a timestamp containing the progress per page is downloaded at each page so in case the download is interrupted there is no need to re-download already downloaded Tweets. The download is done either when the maximum amount of tweets is reached or when there are no more tweets that satisfy the query parameters to download. 

```console
Downloading tweets...
Current progress saved at: Tennis_project_downloads\temp_Tennis_players_project_08032022_171311.csv
Ending page 1 with next_token=b26v89c19zqg8o3fpz2m17r4qqlvzhsejuwhysusao1a5. 496 tweets retrieved (496 total)
Current progress saved at: Tennis_project_downloads\temp_Tennis_players_project_08032022_171311.csv
Tweets download done. A total of 766 tweets were retrieved.
csv files: Tennis_project_downloads\Tennis_players_project_tweets_08032022_171311.csv, Tennis_project_downloads\Tennis_players_project_places_08032022_171311.csv, and Tennis_project_downloads\Tennis_players_project_authors_08032022_171311.csv were generated

```

The previous method saves three dataframes in csv format:

| File                       | Description                                                                             |
|----------------------------|-----------------------------------------------------------------------------------------|
| {Project name}_tweets.csv  | Tweets table. Each row represents an individual tweet with its corresponding attributes |
| {Project name}_places.csv  | Places table. Each row represents a location from which one or more tweets came from    |
| {Project name}_authors.csv | Authors table. Each row represents a user that wrote one or more tweets                 |

The corresponding dataframes can be accessed as the attributes: ```gtd.tweetds_df ```, ```gtd.places_df ```, and ```gtd.authors_df ```, which are pandas DataFrames:

```python
gtd.tweetds_df.head()
```
|     | created_at               | text                                                                                                                                                                                                       |                  id |     conversation_id |           author_id | geo                              | public_metrics                                                            | place_id         | date                      | likes | replies | retweets |
|----:|:-------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------:|--------------------:|--------------------:|:---------------------------------|:--------------------------------------------------------------------------|:-----------------|:--------------------------|------:|--------:|---------:|
|   0 | 2022-07-06T23:53:53.000Z | @christophclarey Nadal won his 1st GS on his 1st attempt at RG in 05 when he was 19.  It was a watershed moment.  Conversely, in 86 TM was never the same after his loss to IL.  As for TF time will tell. | 1544832034429816832 | 1544773073928425472 |          2200548513 | {'place_id': '01fb944c0dff3d86'} | {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0} | 01fb944c0dff3d86 | 2022-07-06 23:53:53+00:00 |     0 |       0 |        0 |
|   1 | 2022-07-06T23:43:21.000Z | @guygavrielkay What a beautiful image. And appropriate, given the number of people who talk about Nadal as if he's Aslan. :)                                                                               | 1544829383092879360 | 1544752022171586560 |            14703552 | {'place_id': '58a65d4a55d1b7f6'} | {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0} | 58a65d4a55d1b7f6 | 2022-07-06 23:43:21+00:00 |     0 |       0 |        0 |
|   2 | 2022-07-06T23:32:12.000Z | @AnnaK_4ever Agreed. I think people are harder on Fritz because of all Nadal’s fake injuries.                                                                                                              | 1544826579989184512 | 1544767392626212866 |           388514822 | {'place_id': '64ab889e24887e12'} | {'retweet_count': 0, 'reply_count': 1, 'like_count': 1, 'quote_count': 0} | 64ab889e24887e12 | 2022-07-06 23:32:12+00:00 |     1 |       1 |        0 |
|   3 | 2022-07-06T23:25:08.000Z | @rollxadvertisers Grow Your Buissness #itshappening #HBDIconOfMillionsDhoni #Nadal #cryptocurrencies https://t.co/FeBknzlnk8                                                                               | 1544824799540793347 | 1544824799540793347 | 1535277320830865408 | {'place_id': '00cc0d5640394308'} | {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0} | 00cc0d5640394308 | 2022-07-06 23:25:08+00:00 |     0 |       0 |        0 |
|   4 | 2022-07-06T23:20:47.000Z | Which kind play b this 😅  #Nadal #itshappening Jordan/ Inaki Williams/. KNUST SRC https://t.co/3qshCRv7tg                                                                                                 | 1544823707448840194 | 1544823707448840194 |  953033567549915136 | {'place_id': '0085c4a6640325a8'} | {'retweet_count': 3, 'reply_count': 0, 'like_count': 2, 'quote_count': 0} | 0085c4a6640325a8 | 2022-07-06 23:20:47+00:00 |     2 |       0 |        3 |
                                                                                                                                                                                                     |                     |                     |                     |                                  |                                                                           |                  |                           |       |         |          |
```python
gtd.places_df.head()
```
|    | name         | id               | country_code   | full_name            | place_type   | country       | geo                                                                                                 |
|---:|:-------------|:-----------------|:---------------|:---------------------|:-------------|:--------------|:----------------------------------------------------------------------------------------------------|
|  0 | Peñalolén    | 01fb944c0dff3d86 | CL             | Peñalolén, Chile     | city         | Chile         | {'type': 'Feature', 'bbox': [-70.5912832, -33.5127583, -70.4388729, -33.4591303], 'properties': {}} |
|  1 | Amherst      | 58a65d4a55d1b7f6 | CA             | Amherst, Nova Scotia | city         | Canada        | {'type': 'Feature', 'bbox': [-64.232955, 45.802245, -64.179066, 45.844832], 'properties': {}}       |
|  2 | Collierville | 64ab889e24887e12 | US             | Collierville, TN     | city         | United States | {'type': 'Feature', 'bbox': [-89.7444626, 35.006217, -89.640889, 35.110826], 'properties': {}}      |
|  3 | Punjab       | 00cc0d5640394308 | PK             | Punjab, Pakistan     | admin        | Pakistan      | {'type': 'Feature', 'bbox': [69.328873, 27.708226, 75.382124, 34.019989], 'properties': {}}         |
|  4 | Oyarifa      | 0085c4a6640325a8 | GH             | Oyarifa, Ghana       | city         | Ghana         | {'type': 'Feature', 'bbox': [-0.2508272, 5.6545401, -0.1145835, 5.7836066], 'properties': {}}       |

```python
gtd.authors_df.head()
```
|    | name                          | public_metrics                                                                                | location                       | username        |                  id |
|---:|:------------------------------|:----------------------------------------------------------------------------------------------|:-------------------------------|:----------------|--------------------:|
|  0 | Gary Counsil                  | {'followers_count': 123, 'following_count': 581, 'tweet_count': 4368, 'listed_count': 0}      | New York, N.Y. Santiago, Chile | garyecounsil    |          2200548513 |
|  1 | Frederick Lane 🇺🇸🇮🇪🏴󠁧󠁢󠁳󠁣󠁴󠁿🇺🇦 | {'followers_count': 4569, 'following_count': 5025, 'tweet_count': 94035, 'listed_count': 108} | Brooklyn, NY                   | fsl3            |            14703552 |
|  2 | Chris Sahm                    | {'followers_count': 225, 'following_count': 372, 'tweet_count': 6703, 'listed_count': 9}      | New Palestine, IN              | ChrisSahm       |           388514822 |
|  3 | Roll-X Advertisers            | {'followers_count': 55, 'following_count': 182, 'tweet_count': 26, 'listed_count': 0}         | Islamabad, Pakistan            | rollxadvertiser | 1535277320830865408 |
|  4 | N E N E 💎 O S U Q U A Y E 💭 | {'followers_count': 1661, 'following_count': 1257, 'tweet_count': 6570, 'listed_count': 0}    | Accra, Ghana                   | sirdesmond3     |  953033567549915136 |

## Get replies

The get_tweets() method can retrieve tweets that generate replies that may not satisfy the query parameters and hence, these would not show up in the results.
Call this method to get the replies to the downloaded tweests. ***Warning: proceed with caution as this method can increase significantly  the API calls. Make sure to cap the maximum amount of tweets by using the max_replies parameter***

Example:
```python
gtd.get_replies(max_replies=20)
```
```console
Downloading replies... this might take some time
getting replies for tweet 1 out of 189 (total replies so far:0)
Current progress saved at: downloads\temp_Tennis_players_project_08032022_174714.csv
getting replies for tweet 2 out of 189 (total replies so far:14)
Current progress saved at: downloads\temp_Tennis_players_project_08032022_174714.csv
Replies download done. 28 reply tweets were downloaded
```

The resulting replies dataframe can be accessed as ```gtd.repliesdf ```. Notice the total amount of tweets went slightly over the maximum. This is a result of the impossibility to determine the actual amount of tweets that are going to be retrieved from each API call. 

## Search parameters in csv file

Some users of this library might want to make use of it by writing as little code as possible. For this cases, the function ```tweets_from_csv()``` is available.
To use it, you need to set up a table in a csv containing the following information. *** Please keep the row names as indicated. The description column is not needed ***:

|    | parameter           | value                     | description                                                                                                                                                                                                                                                                   |
|---:|:--------------------|:--------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  0 | query               | (Nadal) OR (Rafael Nadal) | use single space for AND operator and use ''OR" for the OR operator. Example= apples OR (grapes  bananas). For more information and operators go to: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query#build                            |
|  1 | start_time          | 2022-07-06T00:00:00z      | oldest possible date and time of the retrieved tweets in YYYY-MM-DDTHH:mm:ssZ format                                                                                                                                                                                          |
|  2 | end_time            | 2022-07-07T00:00:00z      | the most recient possible date and time for retrieved tweets in YYYY-MM-DDTHH:mm:ssZ format                                                                                                                                                                                   |
|  3 | max_tweets          | 1000                      | total maximum amount of tweets.                                                                                                                                                                                                                                               |
|  4 | max_tweets_page     | 500                       | maximum amount of tweets per tweet page. Must be between 10 and 500                                                                                                                                                                                                           |
|  5 | language            | en                        | if specific language is needed                                                                                                                                                                                                                                                |
|  6 | place               | nan                       | if specific place is needed                                                                                                                                                                                                                                                                              |
|  7 | include_retweets    | no                        | "yes" or "no" depending on whether the user wants                                                                                                                                                                                                                             |
|  8 | only_georreferenced | yes                       | "yes" or "no" depending on whether the user wants                                                                                                                                                                                                                             |
|  9 | filename            | nan                       | The name of the file. A timestamp will be added at the end to avoid file overwriting when file name stays the same                                                                                                                                                            |
| 10 | wordcloud           | no                        | "yes" or "no" depending on whether the user wants to get a wordcoud or not                                                                                                                                                                                                    |
| 11 | stopwords           | no                        | comma separated words to be exlcuded from wordcloud. Example:"http","https", "TN", "Nashville", "County", "Putnam", "tornado", "tornadoes", "tennesse"                                                                                                                        |
| 12 | barplot             | no                        | "yes" or "no" depending on whether the user wants to get a barplot or not                                                                                                                                                                                                     |

After building the parameters table and saving it in a csv file, you can call the ```tweets_from_csv()``` by passing the csv file as a parameter:

```python
gtd.tweets_from_csv('parameters.csv')
```