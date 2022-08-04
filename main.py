from gtdownloader import TweetDownloader

if __name__ == '__main__':

    gtd = TweetDownloader(
        name='Pandemic_beginning',
        credentials='credentials/twitter_keys.yaml',
        output_folder='downloads'
    )

    #gtd.tweets_from_csv('parameters/parameters.csv')
    # accessing tweets data frame
    #gtd.tweets_df.head()

    # between the dates 07/23/2022 and 07/29/2022
    gtd.get_tweets(
        query='pandemic',
        lang='en',
        start_time='03/8/2020',
        end_time='03/16/2020',
        max_tweets=50000
    )
    gtd.map_animation(time_unit='day')
    gtd.interactive_map()
    gtd.interactive_map_agg()
    gtd.preview_tweet_locations()
    gtd.wordcloud()
    print('hey')

