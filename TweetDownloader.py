"""
COMPLEX AND SUSTAINABLE URBAN NETWORKS LAB
Twitter API usage for tweets download
@author: Juan Acosta
"""

import time
import pandas as pd
from datetime import datetime, timedelta
from searchtweets import collect_results, load_credentials


def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%Sz')
        return date_text
    except ValueError:
        try:
            date_obj = datetime.strptime(date_text, '%m/%d/%Y %H:%M:%S')
        except ValueError:
            try:
                date_obj = datetime.strptime(date_text, '%m/%d/%Y')
            except ValueError:
                date_obj = datetime.strptime(date_text, '%m/%d/%Y %H:%M:')

        return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")


class TweetDownloader:
    """
    Instantiate the tweet downloads class.
    """

    def __init__(self, credentials,
                 name='Project_{}'.format(datetime.now().strftime('%m%d%Y_%H%M%S')),
                 output_folder=''):
        self.name = name
        self.credentials = credentials
        self.output_folder = output_folder
        self.tweets = None
        self.authors = None
        self.places = None
        self.replies = None
        self.search_args = load_credentials(self.credentials,
                                            yaml_key="search_tweets_v2",
                                            env_overwrite=False)
        self.timestamp = None

    def get_tweets(self, query,
                   start_time=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%Sz"),
                   end_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                   lang=None,
                   include_retweets=False,
                   place=None,
                   include_replies=False,
                   max_replies=10,
                   temp_replies=True,
                   save_replies=False,
                   max_tweets=10, max_page=500, save_temp=True, save_final=False):

        ### Query parameters

        query = '({})'.format(query)

        filename = self.name

        if lang:
            query += ' (lang:{})'.format(lang)
        if place:
            query += ' (place_country:{})'.format(place)
        if not include_retweets:
            query += ' (-is:retweet)'

        max_page = max_tweets if max_tweets <= max_page else max_page

        print(query)
        query_params = {'query': query,
                        'start_time': validate_date(start_time),
                        'end_time': validate_date(end_time),
                        'expansions': 'geo.place_id,author_id',
                        'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
                        'tweet.fields': 'created_at,author_id,id,public_metrics,conversation_id',
                        'user.fields': 'id,location,name,username,public_metrics',
                        'max_results': max_page
                        }

        ### initializes a list to store retrieved tweet pages
        list_tweet_pages = []
        ### initializes tweet page count
        page_count = 1
        ### initializes retrieved tweets count
        tweet_count = 0

        ### Creates a timestamp to avoid overwriting old files
        self.timestamp = datetime.now().strftime('_%m%d%Y_%H%M%S.csv')
        ### Creates data frames to store tweets, locations, and author data

        df_tweets = pd.DataFrame()
        df_places = pd.DataFrame()
        df_authors = pd.DataFrame()

        ### loop that ends whenever desired number of tweets is retrieved
        while True:

            ### Collect results according to query parameters, tweets per page...
            ### ... and authendication credentials

            tweets_page = collect_results(query_params, max_tweets=max_page,
                                          result_stream_args=self.search_args)
            if (len(tweets_page) != 0):  ## ensures we don't process a blank page

                ### Adds retrieved page of tweets to list of pages
                list_tweet_pages.append(tweets_page)

                ### Adds number of retrieved tweets to tweet count
                tweet_count += tweets_page[0]['meta']['result_count']

                df_page = pd.DataFrame(tweets_page[0]['data'])
                df_page_authors = pd.DataFrame(tweets_page[0]['includes']['users'])

                df_tweets = pd.concat([df_tweets, df_page])
                df_authors = pd.concat([df_authors, df_page_authors])

                try:
                    df_page_places = pd.DataFrame(tweets_page[0]['includes']['places'])
                    df_places = pd.concat([df_places, df_page_places])
                except KeyError:
                    print('No places on this page...')
                    print('Building DataFrame from Tweet pages...')

                ### resets index of dataframes to avoid redundancy after concatenation
                df_tweets.reset_index(drop=True, inplace=True)
                df_places.reset_index(drop=True, inplace=True)
                df_authors.reset_index(drop=True, inplace=True)

                ## saving temporal dataframes
                if (save_temp):
                    df_tweets.to_csv('temp_' + filename + self.timestamp, index=False)
                    df_places.to_csv('temp_' + filename + '_places' + self.timestamp, index=False)
                    df_authors.to_csv('temp_' + filename + '_authors' + self.timestamp, index=False)

                ### Checks whether there are more pages and goes onto the next page...
                try:
                    print('Ending page %s with next_token=%s. %s tweets retrieved (%s total)' % (
                        page_count, tweets_page[0]['meta']['next_token'], tweets_page[0]['meta']['result_count'],
                        tweet_count))
                    next_token = tweets_page[0]['meta']['next_token']
                    query_params['next_token'] = next_token
                    page_count += 1
                    time.sleep(5)

                ### ...or if final page is reached then the loop ends
                except KeyError:
                    print('Ending page %s. This was the final page. %s tweets retrieved' % (page_count, tweet_count))
                    break
                ### Ends loop if maximum number of tweets is reached
                if (tweet_count >= max_tweets):
                    print('Intended amount of tweets reached. %s tweets retrieved. Goal was %s' % (
                        tweet_count, max_tweets))
                    break
            else:
                print('This tweets page had 0 tweets')

        ### Loop that goes through the tweet pages and stores data in DataFrames
        print('Building DataFrame from Tweet pages...')

        df_tweets = pd.DataFrame()
        df_places = pd.DataFrame()
        df_authors = pd.DataFrame()

        for page in list_tweet_pages:
            df_page = pd.DataFrame(page[0]['data'])
            df_page_authors = pd.DataFrame(page[0]['includes']['users'])

            try:
                df_page_places = pd.DataFrame(page[0]['includes']['places'])
                df_places = pd.concat([df_places, df_page_places])
            except KeyError:
                print('No places on this page...')
                print('Building DataFrame from Tweet pages...')
            df_tweets = pd.concat([df_tweets, df_page])
            df_authors = pd.concat([df_authors, df_page_authors])

        ### resets index of dataframes to avoid redundancy after concatenation
        df_tweets.reset_index(drop=True, inplace=True)
        df_places.reset_index(drop=True, inplace=True)
        df_authors.reset_index(drop=True, inplace=True)

        self.tweets = df_tweets
        self.places = df_places
        self.authors = df_authors

        print('Done')

        if (save_final):
            ## saving final dataframes
            df_tweets.to_csv(filename + self.timestamp, index=False)
            df_places.to_csv(filename + '_places' + self.timestamp, index=False)
            df_authors.to_csv(filename + '_authors' + self.timestamp, index=False)

            print('csv files {} and {} were generated'.format(filename + self.timestamp,
                                                              filename + '_places' + self.timestamp))

        if (include_replies):
            print('Preparing to get tweet replies...')
            df_replies = self.get_replies(max_replies=max_replies,
                                          save_temp=temp_replies, save_final=save_replies)
            return df_tweets, df_places, df_authors, df_replies

        else:
            return df_tweets, df_places, df_authors

    def get_replies(self, max_replies=10, save_temp=True, save_final=False):

        list_tweet_pages = []
        page_count = 1
        tweet_count = 0

        df_tweets_rep = pd.DataFrame()

        for conversation_id in self.tweets.conversation_id:

            query = 'conversation_id:{}'.format(conversation_id)

            ### Maximum amount of tweets to retrieve. This is only the maximum and not a
            ### guaranteed amount of results
            max_tweets_total = max_replies
            ### Maximum tweets retrieved on each "page". Must be integer between 10 and 500
            max_tweets_page = max_replies if max_replies <= 500 else 500

            ### query parameters. For info see:
            ## https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all

            query_params = {'query': query,
                            'start_time': '2007-01-01T00:00:00z',
                            'end_time': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                            'expansions': 'author_id',
                            'tweet.fields': 'created_at,author_id,id,conversation_id',
                            'user.fields': 'id,name,username,public_metrics',
                            'max_results': max_tweets_page
                            }

            while True:
                tweets_page = collect_results(query_params, max_tweets=max_tweets_page,
                                              result_stream_args=self.search_args)
                list_tweet_pages.append(tweets_page)
                print('downloading replies to ', query)
                time.sleep(1)
                if (len(tweets_page) > 0):
                    tweet_count += tweets_page[0]['meta']['result_count']

                    df_page = pd.DataFrame(tweets_page[0]['data'])
                    df_tweets_rep = pd.concat([df_tweets_rep, df_page])
                    df_tweets_rep.reset_index(drop=True, inplace=True)
                    df_tweets_rep['date_time'] = pd.to_datetime(df_tweets_rep.created_at)
                    if save_temp:
                        df_tweets_rep.to_csv('temp_' + self.name + '_places' + self.timestamp, index=False)

                    try:
                        print('Ending page %s with next_token=%s. %s tweets retrieved (%s total)' % (
                            page_count, tweets_page[0]['meta']['next_token'], tweets_page[0]['meta']['result_count'],
                            tweet_count))
                        next_token = tweets_page[0]['meta']['next_token']
                        query_params['next_token'] = next_token
                        page_count += 1
                    except KeyError:
                        print('Ending page %s. This was the final page. %s tweets retrieved' % (
                            page_count, tweet_count))
                        break

                    if (tweet_count >= max_tweets_total):
                        print('Intended amount of tweets reached. %s tweets retrieved. Goal was %s' % (
                            tweet_count, max_tweets_total))
                        break
                else:
                    print('This conversation has no more replies')
                    break

        if save_final:
            df_tweets_rep.to_csv(self.name + '_places' + self.timestamp, index=False)

        self.replies = df_tweets_rep
        return df_tweets_rep
