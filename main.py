from gtdownloader import TweetDownloader

if __name__ == '__main__':

    gtd = TweetDownloader(
        name='Tennis_players_project',
        credentials='credentials/twitter_keys.yaml',
        output_folder='downloads'
    )

    gtd.tweets_from_csv('parameters/parameters.csv')
    # accessing tweets data frame
    gtd.tweets_df.head()

    # between the dates 07/23/2022 and 07/29/2022
'''    gtd.get_tweets(
        query='(Nadal) OR (Rafael Nadal)',
        lang='en',
        start_time='07/06/2022',
        end_time='07/07/2022',
        max_tweets=1000
    )'''

