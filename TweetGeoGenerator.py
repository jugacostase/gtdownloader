import os
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
        self.filename = downloader.name
        self.timestamp = downloader.timestamp
        self.tweets_centroid = None
        self.places_centroid = None
        self.authors_centroid = None
        self.tweets_bbox = None
        self.places_bbox = None
        self.authors__bbox = None

    def create_gdf(self):
        self.tweets_df['place_id'] = self.tweets_df.geo.apply(lambda x: x['place_id'])
        # Creates date column in date format
        self.tweets_df['date'] = pd.to_datetime(self.tweets_df.created_at)
        self.tweets_df['date'] = self.tweets_df.date.dt.strftime('%m/%d/%Y')
        self.tweets_df['date'] = pd.to_datetime(self.tweets_df['date'])

        # Create Polygon from bboxes in the places dataframe before creating geodataframe
        self.places_df['geometry'] = self.places_df['geo'].apply(extract_bbox_polygon)
        self.places_bbox = gpd.GeoDataFrame(self.places_df, crs="EPSG:4326")
        self.places_bbox.rename(columns={'id': 'place_id'}, inplace=True)

        print(0)

    def save_tweets_shp(self, save_path='', geo_type='centroids'):
        os.chdir(os.path.dirname(__file__))
        self.tweets_df.rename(columns={'id': 'tweet_id'}, inplace=True)
        if geo_type == 'centroids':
            self.compute_centroids()
            self.tweets_centroid = pd.merge(self.places_centroid, self.tweets_df, on='place_id')
            self.tweets_centroid.rename(columns={'id':'place_id'}, inplace=True)
            self.tweets_centroid.drop(columns=['geo_x', 'geo_y'], inplace=True)
            print(os.path.join(os.getcwd()), save_path)
            shape_filename = os.path.join(os.getcwd(), save_path, self.filename + '_tweets_' + '.shp')
            self.tweets_centroid.to_file(shape_filename)
        elif geo_type == 'bbox':
            self.tweets_bbox = pd.merge(self.places_bbox, self.tweets_df, on='place_id')
            self.tweets_bbox.drop(columns=['geo_x', 'geo_y'])
            print(os.path.join(os.getcwd()), save_path)



    def compute_centroids(self):
        self.places_centroid = self.places_bbox
        self.places_centroid['geometry'] = self.places_centroid.to_crs("EPSG:3395").geometry.centroid
        self.places_centroid = self.places_centroid.to_crs("EPSG:4326")
        self.places_centroid.rename(columns={'id': 'place_id'}, inplace=True)
