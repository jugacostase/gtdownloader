from gtdownloader.downloader import TweetDownloader

td = TweetDownloader(bearer_token='AAAAAAAAAAAAAAAAAAAAAA8cTQEAAAAA8ErByhz3ZyGH8XfuCJkGqH6eWeQ%3D2d4m6xmtnyI78jLt1nyc9IcKP4sGRThNxuCwJUBfFt6vMEGBAi', output_folder='../exports')
td.get_tweets(query='dog', max_tweets=10, start_time='01/01/2017', end_time='12/31/2022', has_geo=False)

def test_tweets_gdf_c():
    gdf = td.tweets_to_gdf()
    assert gdf.geometry.shape[0] > 0

def test_tweets_gdf_b():
    gdf = td.tweets_to_gdf('bbox')
    assert gdf.geometry.shape[0] > 0

def test_places_gdf_c():
    gdf = td.places_to_gdf()
    assert gdf.geometry.shape[0] >= 0

def test_places_gdf_b():
    gdf= td.places_to_gdf('bbox')
    assert gdf.geometry.shape[0] >= 0



