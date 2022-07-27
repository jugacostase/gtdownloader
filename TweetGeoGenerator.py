import os
import ast

import numpy as np
import pandas as pd
import geopandas as gpd

from shapely.geometry import Polygon
import plotly.express as px

import matplotlib.pyplot as plt



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
        # Create Polygon from bboxes in the places dataframe before creating geodataframe
        self.places_df['geometry'] = self.places_df['geo'].apply(extract_bbox_polygon)
        self.places_bbox = gpd.GeoDataFrame(self.places_df, crs="EPSG:4326")
        self.places_bbox.rename(columns={'id': 'place_id'}, inplace=True)

    def save_tweets_shp(self, save_path='', geo_type='centroids'):
        os.chdir(os.path.dirname(__file__))
        self.tweets_df.rename(columns={'id': 'tweet_id'}, inplace=True)
        if geo_type == 'centroids':
            self.compute_centroids()
            shape_filename = os.path.join(os.getcwd(), save_path, self.filename + '_tweets_centroids' + '.shp')
            tweets_centroid = self.tweets_centroid
            tweets_centroid['date'] = tweets_centroid.date.dt.strftime('%m/%d/%Y %H:%M%:%s')
            tweets_centroid.drop(columns=['public_metrics', 'created_at'], inplace=True)
            tweets_centroid.rename(columns={'country_code': 'cntry_code',
                                            'conversation_id': 'conv_id',
                                            'name': 'place',
                                            'full_name': 'full_place'}, inplace=True)
            tweets_centroid.to_file(shape_filename)
            print('Shapefile with tweet centroids saved to file:', shape_filename)
        elif geo_type == 'bbox':
            self.tweets_bbox = pd.merge(self.places_bbox, self.tweets_df, on='place_id')
            self.tweets_bbox.drop(columns=['geo_x', 'geo_y'])
            self.tweets_bbox.rename(columns={'id': 'place_id'}, inplace=True)
            tweets_bbox = self.tweets_bbox
            tweets_bbox['date'] = tweets_bbox.date.dt.strftime('%m/%d/%Y %H:%M%:%s')
            tweets_bbox.rename(columns={'country_code': 'cntry_code',
                                        'conversation_id': 'conv_id',
                                        'name': 'place',
                                        'full_name': 'full_place'}, inplace=True)
            shape_filename = os.path.join(os.getcwd(), save_path, self.filename + '_tweets_bboxes' + '.shp')
            tweets_bbox.to_file(shape_filename)
            print('Shapefile with tweet bounding boxes saved to file:', shape_filename)



    def compute_centroids(self):
        self.places_centroid = self.places_bbox.copy()
        self.places_centroid['geometry'] = self.places_centroid.to_crs("EPSG:3395").geometry.centroid
        self.places_centroid = self.places_centroid.to_crs("EPSG:4326")
        self.places_centroid.rename(columns={'id': 'place_id'}, inplace=True)
        self.tweets_centroid = pd.merge(self.places_centroid, self.tweets_df, on='place_id')
        self.tweets_centroid.drop(columns=['geo_x', 'geo_y'], inplace=True)

    def simple_tweets_map(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        base = world.plot(color='white', edgecolor='black')
        self.compute_centroids()
        self.tweets_centroid.plot(ax=base, marker='o', color='red', markersize=5)
        plt.show()


    def plot_tweets_points(self):

        self.compute_centroids()
        plot_gdf = self.tweets_centroid
        plot_gdf['lon'] = plot_gdf.geometry.x
        plot_gdf['lat'] = plot_gdf.geometry.y

        fig = px.scatter_geo(plot_gdf[['lat', 'lon', 'text', 'date', 'likes', 'name']],
                             lat='lat', lon='lon', color="name", hover_name="name", size='likes',
                             projection="natural earth")
        fig.show()

    def plot_tweets_aggregated(self):
        # world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        # base = world.plot(color='white', edgecolor='black')
        # self.compute_centroids()
        # self.tweets_centroid.plot(ax=base, marker='o', color='red', markersize=5)
        # plt.show()
        self.compute_centroids()

        plot_gdf = self.tweets_centroid.dissolve(by='place_id', aggfunc={'name': 'first',
                                                                         'likes': 'count',
                                                                         'text': 'first',
                                                                         'date': 'first'})
        plot_gdf['lon'] = plot_gdf.geometry.x
        plot_gdf['lat'] = plot_gdf.geometry.y

        fig = px.scatter_geo(plot_gdf[['lat', 'lon', 'text', 'date', 'likes', 'name']],
                             lat='lat', lon='lon', color="name", hover_name="name", size='likes',
                             projection="natural earth")
        fig.show()


