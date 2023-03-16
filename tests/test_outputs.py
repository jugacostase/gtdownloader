import pytest
import matplotlib.pyplot as plt
from gtdownloader.downloader import TweetDownloader

@pytest.fixture(scope="session")
def apicall():
    td = TweetDownloader(env_token='TWITTER_BEARER_TOKEN')
    td.get_tweets(query='dog', max_tweets=10, start_time='01/01/2017', end_time='12/31/2022', has_geo=True,
                  save_temp=False, save_final=False)
    return td

def test_plots(apicall):
    apicall.preview_tweet_locations()
    apicall.interactive_map()
    apicall.interactive_map_agg()
    apicall.wordcloud()
    apicall.wordcloud(bar_plot=True)
    apicall.map_animation(time_unit='day')
    apicall.plot_heatmap()



