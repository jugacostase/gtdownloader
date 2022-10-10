from gtdownloader import TweetDownloader

if __name__ == '__main__':

    gtd = TweetDownloader(
        name='Bike_commuting',
        credentials='credentials/twitter_keys.yaml',
        output_folder='downloads'
    )

    #gtd.tweets_from_csv('parameters/parameters.csv')
    # accessing tweets data frame
    #gtd.tweets_df.head()

    # between the dates 07/23/2022 and 07/29/2022
    gtd.get_tweets(
        query='bike commuting',
        lang='en',
        start_time='01/01/2019',
        end_time='12/31/2021',
        max_tweets=1000
    )
    gtd.map_animation(time_unit='month')
    gtd.interactive_map()
    gtd.interactive_map_agg()
    gtd.preview_tweet_locations()
    gtd.wordcloud(custom_stopwords=['bike', 'commuting', 'http', 'https'], background_color='white')
    print('The End')

