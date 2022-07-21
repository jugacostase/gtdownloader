import ast
import numpy as np
import pandas as pd
import geopandas as gpd


def get_attribute_id(x, attribute_id):
    try:
        return ast.literal_eval(x)[attribute_id]
    except ValueError:
        return np.nan


class TweetGeoGenerator:

    def __init__(self, downloader):
        self.tweets_df = downloader.tweets_df
        self.authors_df = downloader.authors_df
        self.places_df = downloader.places_df
        self.tweets_gdf = None

    def create_gdf(self):
        self.tweets_df['place_id'] = self.tweets_df.geo.apply(lambda x: x['place_id'])
        # Creates date column in date format
        self.tweets_df['date'] = pd.to_datetime(self.tweets_df.created_at)
        self.tweets_df['date'] = self.tweets_df.date.dt.strftime('%m/%d/%Y')
        self.tweets_df['date'] = pd.to_datetime(self.tweets_df['date'])
        print(0)
