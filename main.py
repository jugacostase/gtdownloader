from tgdownloader.downloader import TweetDownloader

if __name__ == '__main__':

    tgd = TweetDownloader(name='Messi_test', credentials='../credentials/twitter_keys.yaml',
                                 output_folder='../downloads')

    tgd.get_tweets('Cristiano Ronaldo', lang='en', max_tweets=400,
                          start_time='07/23/2022', end_time='07/29/2022')

    tgd.tweets_to_shp('../exports')
    tgd.places_to_shp('../exports', 'centroids')
    tgd.preview_tweet_locations()
    tgd.interactive_map()
    tgd.interactive_map_aggregated()
    tgd.plot_heatmap()
    tgd.map_animation('day')
    tgd.wordcloud()

    #tgd.wordcloud()
    #tgd.tweets_from_csv(path='search_params/parameters.csv')
