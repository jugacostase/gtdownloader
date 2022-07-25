from TweetDownloader import TweetDownloader
from TweetGeoGenerator import TweetGeoGenerator

if __name__ == '__main__':

    downloader = TweetDownloader(credentials='credentials/twitter_keys.yaml', output_folder='downloads')

    downloader.get_tweets('Petro', lang='es', place='CO', max_tweets=600,
                          include_replies=False, start_time='07/17/2021',
                                                    end_time='07/21/2021')

    #downloader.tweets_from_csv('parameters/parameters.csv')

    tgeo = TweetGeoGenerator(downloader)
    tgeo.create_gdf()
    tgeo.save_tweets_shp()
