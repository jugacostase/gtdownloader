import pytest
from gtdownloader.downloader import TweetDownloader

@pytest.fixture(scope="session")
def apicall():
    td = TweetDownloader(
        bearer_token='AAAAAAAAAAAAAAAAAAAAAA8cTQEAAAAA8ErByhz3ZyGH8XfuCJkGqH6eWeQ%3D2d4m6xmtnyI78jLt1nyc9IcKP4sGRThNxuCwJUBfFt6vMEGBAi')
    td.get_tweets(query='dog', max_tweets=10, start_time='01/01/2017', end_time='12/31/2022', has_geo=False, save_temp=False)
    return td


def test_tweets_gdf_c(apicall):
    gdf = apicall.tweets_to_gdf()
    assert gdf.geometry.shape[0] > 0


def test_tweets_gdf_b(apicall):
    gdf = apicall.tweets_to_gdf('bbox')
    assert gdf.geometry.shape[0] > 0


def test_places_gdf_c(apicall):
    gdf = apicall.places_to_gdf()
    assert gdf.geometry.shape[0] >= 0


def test_places_gdf_b(apicall):
    gdf = apicall.places_to_gdf('bbox')
    assert gdf.geometry.shape[0] >= 0
