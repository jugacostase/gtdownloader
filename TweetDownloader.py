"""
COMPLEX AND SUSTAINABLE URBAN NETWORKS LAB
Twitter API usage for tweets download
@author: Juan Acosta
"""
import os
import ast
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from searchtweets import collect_results, load_credentials
from TweetGeoGenerator import TweetGeoGenerator

def get_attribute_id(x, attribute_id):
    try:
        return ast.literal_eval(x)[attribute_id]
    except ValueError:
        return np.nan

def get_attribute_from_dict(x, attribute_id):
    try:
        return x[attribute_id]
    except TypeError:
        return np.nan

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
        self.tweets_df = None
        self.authors_df = None
        self.places_df = None
        self.replies_df = None
        self.search_args = load_credentials(self.credentials,
                                            yaml_key="search_tweets_v2",
                                            env_overwrite=False)
        self.timestamp = None

    def tweets_from_query(self, query_params, max_page, save_temp, max_tweets, reply_mode=False):
        ### initializes a list to store retrieved tweet pages
        list_tweet_pages = []
        ### initializes tweet page count
        page_count = 1
        ### initializes retrieved tweets count
        tweet_count = 0
        ### count to stop algorithm when search has no results
        zeros_count = 0

        filename = self.name

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
                    #print('No places on this page...')
                    #print('Building DataFrame from Tweet pages...')
                    pass

                ### resets index of dataframes to avoid redundancy after concatenation
                df_tweets.reset_index(drop=True, inplace=True)
                df_places.reset_index(drop=True, inplace=True)
                df_authors.reset_index(drop=True, inplace=True)

                ## saving temporal dataframes
                if (save_temp & (not reply_mode)):
                    df_tweets.to_csv(os.path.join(self.output_folder, 'temp_' + filename + self.timestamp),
                                     index=False)
                    df_places.to_csv(os.path.join(self.output_folder, 'temp_' + filename + '_places' + self.timestamp),
                                     index=False)
                    df_authors.to_csv(os.path.join(self.output_folder, 'temp_' + filename + '_authors' + self.timestamp),
                                      index=False)

                if (save_temp & reply_mode):
                    df_tweets.to_csv(os.path.join(self.output_folder, 'temp_' + filename + '_replies' + self.timestamp),
                                     index=False)

                ### Checks whether there are more pages and goes onto the next page...
                try:
                    if(not reply_mode):
                        print('Ending page %s with next_token=%s. %s tweets retrieved (%s total)' % (
                            page_count, tweets_page[0]['meta']['next_token'], tweets_page[0]['meta']['result_count'],
                            tweet_count))
                    next_token = tweets_page[0]['meta']['next_token']
                    query_params['next_token'] = next_token
                    page_count += 1
                    time.sleep(5)

                ### ...or if final page is reached then the loop ends
                except KeyError:
                    #print('Ending page %s. This was the final page. %s tweets retrieved' % (page_count, tweet_count))
                    break
                ### Ends loop if maximum number of tweets is reached
                if ((tweet_count >= max_tweets) & (not reply_mode)):
                    print('Intended amount of tweets reached. %s tweets retrieved. Goal was %s' % (
                        tweet_count, max_tweets))
                    break
            else:
                #print('This tweets page had 0 tweets')
                zeros_count += 1
                if zeros_count > 1:
                    break



        return list_tweet_pages, df_tweets, df_places, df_authors

    def get_tweets(self, query,
                   start_time=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%Sz"),
                   end_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                   lang=None, include_retweets=False, place=None, has_geo=True,
                   max_tweets=10, max_page=500, save_temp=True, save_final=True,
                   save_replies=False, include_replies=False, max_replies=10, temp_replies=True,):

        ### Query parameters

        query = '({})'.format(query)
        ### Creates a timestamp to avoid overwriting old files
        self.timestamp = datetime.now().strftime('_%m%d%Y_%H%M%S.csv')

        filename = self.name

        if lang:
            query += ' (lang:{})'.format(lang)
        if place:
            query += ' (place_country:{})'.format(place)
        if has_geo:
            query += ' (has:geo)'
        if not include_retweets:
            query += ' (-is:retweet)'

        max_page = max_tweets if max_tweets <= max_page else max_page

        query_params = {'query': query,
                        'start_time': validate_date(start_time),
                        'end_time': validate_date(end_time),
                        'expansions': 'geo.place_id,author_id',
                        'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
                        'tweet.fields': 'created_at,author_id,id,public_metrics,conversation_id',
                        'user.fields': 'id,location,name,username,public_metrics',
                        'max_results': max_page
                        }

        print('Downloading tweets...')

        self.tweets, self.tweets_df, self.places_df, self.authors_df = self.tweets_from_query(query_params, max_page,
                                                                                              save_temp, max_tweets)

        if (save_final):
            self.tweets_df['place_id'] = self.tweets_df.geo.apply(lambda x: get_attribute_from_dict(x, 'place_id'))
            # Creates date column in date format
            self.tweets_df['date'] = pd.to_datetime(self.tweets_df.created_at)
            self.tweets_df['date'] = self.tweets_df.date.dt.strftime('%m/%d/%Y %H:%M%:%S')
            self.tweets_df['date'] = pd.to_datetime(self.tweets_df['date'])

            # Get metrics as separate columns:
            self.tweets_df['likes'] = self.tweets_df.public_metrics.apply(lambda x: x['like_count'])
            self.tweets_df['replies'] = self.tweets_df.public_metrics.apply(lambda x: x['reply_count'])
            self.tweets_df['retweets'] = self.tweets_df.public_metrics.apply(lambda x: x['retweet_count'])

            ## saving final dataframes
            self.tweets_df.to_csv(filename + self.timestamp, index=False)
            self.places_df.to_csv(filename + '_places' + self.timestamp, index=False)
            self.authors_df.to_csv(filename + '_authors' + self.timestamp, index=False)

            print('csv files {} and {} were generated'.format(filename + self.timestamp,
                                                              filename + '_places' + self.timestamp))

        if (include_replies):
            print('Preparing to get tweet replies...')
            if(len(self.tweets) > 0 ):
                self.replies_df = self.get_replies(max_replies=max_replies,
                                                   save_temp=temp_replies, save_final=save_replies)
            else:
                print('There were no tweets to get replies from')

        ## Still unsure about whether to have values to unpack or just have the attributes updated
        #   return self.tweets_df, self.places_df, self.authors_df, self.replies_df

        #else:
        #    return self.tweets_df, self.places_df, self.authors_df,

    def get_replies(self, max_replies=10, save_temp=True, save_final=True):

        df_tweets_rep = pd.DataFrame()

        print('Downloading replies... this might take some time')

        total_tweets = self.tweets_df.shape[0]
        rep_count = 0
        total_replies = 0

        for conversation_id in self.tweets_df.conversation_id:
            rep_count += 1

            print('getting replies for tweet {} out of {} (total replies so far: {})'.format(rep_count,
                                                                                             total_tweets,
                                                                                             total_replies))

            query = 'conversation_id:{}'.format(conversation_id)

            ### Maximum amount of tweets to retrieve. This is only the maximum and not a
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

            time.sleep(5)
            self.replies, df_replies, _, _ = self.tweets_from_query(query_params, max_tweets_page,
                                                                    save_temp, max_replies, reply_mode=True)
            df_tweets_rep = pd.concat([df_tweets_rep, df_replies])

            total_replies = df_tweets_rep.shape[0]

        if save_final:
            df_tweets_rep.to_csv(self.name + '_replies' + self.timestamp, index=False)

        self.replies_df = df_tweets_rep

        return df_tweets_rep

    def build_dataframes(self):
        ### Loop that goes through the tweet pages and stores data in DataFrames
        print('Building DataFrame from Tweet pages...')

        df_tweets = pd.DataFrame()
        df_places = pd.DataFrame()
        df_authors = pd.DataFrame()

        for page in self.tweets:
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

        self.tweets_df = df_tweets
        self.places_df = df_places
        self.authors_df = df_authors

        print('Done')

    def tweets_from_csv(self, path, sep=',', save_temp=True):
        # loading config values into a DataFrame
        df_param = pd.read_csv(path, sep=sep)

        # storing parameters into variables to be passed to the query obj
        query = df_param.query('parameter=="query"')['value'].item()
        start_time = df_param.query('parameter=="start_time"')['value'].item()
        end_time = df_param.query('parameter=="end_time"')['value'].item()
        max_tweets_total = int(df_param.query('parameter=="max_tweets"')['value'].item())
        max_tweets_page = int(df_param.query('parameter=="max_tweets_page"')['value'].item())
        filename = df_param.query('parameter=="filename"')['value'].item()

        ### Query parameters. See the parameters.csv to modify or see the description
        ### of each parameter
        query_params = {'query': query,
                        'start_time': start_time,
                        'end_time': end_time,
                        'expansions': 'geo.place_id,author_id',
                        'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
                        'tweet.fields': 'created_at,author_id,id,public_metrics,conversation_id',
                        'user.fields': 'id,location,name,username,public_metrics',
                        'max_results': max_tweets_page
                        }
        ### Creates a timestamp to avoid overwriting old files
        self.timestamp = datetime.now().strftime('_%m%d%Y_%H%M%S.csv')

        # Gets tweets
        self.tweets_from_query(query_params, max_tweets_page, save_temp, max_tweets_total, reply_mode=False)

    def tweets_to_shp(self, save_path='', geo_type='centroids'):
        tgeo = TweetGeoGenerator(self)
        tgeo.create_gdf()
        tgeo.save_tweets_shp(save_path, geo_type)
        del tgeo

    def preview_tweet_locations(self):
        tgeo = TweetGeoGenerator(self)
        tgeo.create_gdf()
        tgeo.simple_tweets_map()

    def interactive_map(self):
        tgeo = TweetGeoGenerator(self)
        tgeo.create_gdf()
        tgeo.plot_tweets_points()

    def interactive_map_aggregated(self):
        tgeo = TweetGeoGenerator(self)
        tgeo.create_gdf()
        tgeo.plot_tweets_aggregated()


