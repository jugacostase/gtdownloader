from downloader import TweetDownloader

if __name__ == '__main__':

    downloader = TweetDownloader(name='Tests_earthquakes', credentials='credentials/twitter_keys.yaml',
                                 output_folder='downloads')

    downloader.get_tweets('Earthquake', lang='en', max_tweets=400,
                          start_time='07/23/2022', end_time='07/26/2022')

    #downloader.tweets_to_shp('exports')
    #downloader.map_animation('minute')
    #downloader.places_to_shp('exports', 'centro')
    #downloader.wordcloud()
    #downloader.tweets_from_csv(path='search_params/parameters.csv')