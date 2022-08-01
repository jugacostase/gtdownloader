from gtdownloader.downloader import TweetDownloader

td = TweetDownloader(credentials='../credentials/twitter_keys.yaml', output_folder='../exports')


def test_one_page_download_defaults():
    td.get_tweets(query='dog')
    df_tweets = td.tweets_df
    assert df_tweets.shape[0] > 0


def test_download_short():
    td.get_tweets(query='dog', max_tweets=10)
    df_tweets = td.tweets_df
    assert df_tweets.shape[0] > 0


def test_download_short_w_replies():
    td.get_tweets(query='dog', max_tweets=10, include_replies=True,
                  max_replies=10, save_replies=True, temp_replies=False)
    df_replies = td.replies_df
    assert df_replies.shape[0] > 0


def test_download_from_csv():
    td.tweets_from_csv('../parameters/parameters.csv')
    df_tweets = td.tweets_df
    assert df_tweets.shape[0] > 0


