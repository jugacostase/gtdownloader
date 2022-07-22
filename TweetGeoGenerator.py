import ast
import numpy as np
import pandas as pd
from shapely.geometry import Polygon
import geopandas as gpd


def get_attribute_id(x, attribute_id):
    try:
        return ast.literal_eval(x)[attribute_id]
    except ValueError:
        return np.nan

def extract_bbox_polygon(x):
    lon1 = x['bbox'][0]
    lat1 = x['bbox'][1]
    lon2 = x['bbox'][2]
    lat2 = x['bbox'][3]
    polygon = Polygon([(lon1, lat1), (lon1, lat2), (lon2, lat2), (lon2, lat1)])
    return polygon


class TweetGeoGenerator:

    def __init__(self, downloader):
        self.tweets_df = downloader.tweets_df
        self.authors_df = downloader.authors_df
        self.places_df = downloader.places_df
        self.tweets_gdf = None
        self.places_gdf = None
        self.authors_gdf = None
        self.places_bbox = None
        self.places_centroid = None

    def create_gdf(self):
        self.tweets_df['place_id'] = self.tweets_df.geo.apply(lambda x: x['place_id'])
        # Creates date column in date format
        self.tweets_df['date'] = pd.to_datetime(self.tweets_df.created_at)
        self.tweets_df['date'] = self.tweets_df.date.dt.strftime('%m/%d/%Y')
        self.tweets_df['date'] = pd.to_datetime(self.tweets_df['date'])

        # Create Polygon from bboxes in the places dataframe before creating geodataframe
        self.places_df['geometry'] = self.places_df['geo'].apply(extract_bbox_polygon)
        self.places_gdf = gpd.GeoDataFrame(self.places_df, crs="EPSG:4326")

        self.places_gdf.to_file('exports/test_shp.shp')
        print(0)