import os
import time

from gtdownloader.downloader import TweetDownloader

td = TweetDownloader(bearer_token='AAAAAAAAAAAAAAAAAAAAAA8cTQEAAAAA8ErByhz3ZyGH8XfuCJkGqH6eWeQ%3D2d4m6xmtnyI78jLt1nyc9IcKP4sGRThNxuCwJUBfFt6vMEGBAi')


def test_one_page_download_defaults():
    time.sleep(15)
    td.get_tweets(query='dog', save_temp=False)
    df_tweets = td.tweets_df
    assert df_tweets.shape[0] > 0


def test_download_short():
    time.sleep(15)
    td.get_tweets(query='dog', max_tweets=10, start_time='01/01/2017', end_time='12/31/2022', save_temp=False)
    df_tweets = td.tweets_df
    assert df_tweets.shape[0] > 0


def test_download_w_replies():
    time.sleep(15)
    td.get_tweets(query='dog', max_tweets=20, include_replies=True,
                  max_replies=10, save_replies=False, temp_replies=False,
                  start_time='01/01/2017', end_time='12/31/2022', save_temp=False)
    df_replies = td.replies_df
    assert df_replies.shape[0] > 0

def test_download_multi_page():
    time.sleep(15)
    td.get_tweets(query='dog', max_tweets=100, include_replies=False,
                  max_page=10, save_replies=True, temp_replies=False,
                  start_time='01/01/2017', end_time='12/31/2022', save_temp=False)
    df_tweets = td.tweets_df
    assert df_tweets.shape[0] > 0

def test_download_multi_page_w_replies():
    time.sleep(15)
    td.get_tweets(query='dog', max_tweets=20, include_replies=True,
                  max_page=10, save_replies=True, temp_replies=False,
                  start_time='01/01/2017', end_time='12/31/2022', save_temp=False)
    df_replies = td.replies_df
    assert df_replies.shape[0] > 0


def test_download_no_geo():
    time.sleep(15)
    td.get_tweets(query='dog', max_tweets=10, has_geo=False, save_temp=False)
    df_tweets = td.tweets_df
    assert df_tweets.shape[0] > 0

def test_download_from_csv():
    time.sleep(5)
    td.tweets_from_csv('tests/test_parameters.csv', save_temp=False)
    df_tweets = td.tweets_df
    assert df_tweets.shape[0] > 0


