import os

import pandas as pd
import geopandas as gpd

import plotly.express as px
import matplotlib.pyplot as plt

from ._utils.utils import *


class TweetGeoGenerator:
    """Geographical methods class.
    The TweetGeoGenerator leverages the geographical information
    contained in the downloads to generate files and visualizations.

    Parameters
    ----------
    downloader : TweetDownloader
        A tweet downloader object with tweets attribute.

    Attributes
    ----------
    tweets_df : pandas.DataFrame
        Table with the tweets from the attribute tweets
    authors_df : pandas.DataFrame
        Table with the authors from the attribute authors
    places_df : pandas.DataFrame
        Table with the georreferenced locations from the attribute places
    timestamp : str
        A string to append at the end of saved files, so they all have a
        timestamp
    tweets_centroid : geopandas.GeoDataFrame
        A geodataframe containing the tweets. The geometry is the centroid
        of the corresponding tweet location bounding box
    places_centroid : geopandas.GeoDataFrame
        A geodataframe containing the tweet locations. The geometry is the
        centroid of the corresponding location bounding box
    authors_centroid : geopandas.GeoDataFrame
        A geodataframe containing the authors location. The geometry is
        the centroid of the corresponding location bounding box
    tweets_bbox : geopandas.GeoDataFrame
        A geodataframe containing the tweets. The geometry is the
        corresponding tweet location bounding box
    places_bbox : geopandas.GeoDataFrame
        A geodataframe containing the tweet locations. The geometry is the
        corresponding tweet location bounding box
    authors_bbox : geopandas.GeoDataFrame
        A geodataframe containing the tweets authors. The geometry is the
        corresponding location bounding box
    """

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
        self.authors_bbox = None

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
            shape_filename = os.path.join(save_path, self.filename + '_tweets_bboxes' + '.shp')
            tweets_bbox.to_file(shape_filename)
            print('Shapefile with tweet bounding boxes saved to file:', shape_filename)
        else:
            raise ValueError('geo_type not supported. Input either "centroids" or "bbox"')

    def save_places_shp(self, save_path='', geo_type='centroids'):
        if geo_type == 'centroids':
            self.compute_centroids()
            shape_filename = os.path.join(save_path, self.filename + '_places_centroids' + '.shp')
            self.places_centroid.to_file(shape_filename)
            print('Shapefile with places centroids saved to file:', shape_filename)
        elif geo_type == 'bbox':
            shape_filename = os.path.join(save_path, self.filename + '_places_bboxes' + '.shp')
            self.places_bbox.to_file(shape_filename)
            print('Shapefile with places bounding boxes saved to file:', shape_filename)
        else:
            raise ValueError('geo_type not supported. Input either "centroids" or "bbox"')

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
                             lat='lat', lon='lon', color="name", hover_name="text",
                             projection="natural earth")
        fig.show()

    def plot_tweets_aggregated(self):
        self.compute_centroids()

        plot_gdf = self.tweets_centroid.dissolve(by='place_id', aggfunc={'name': 'first',
                                                                         'likes': 'count',
                                                                         'text': 'first',
                                                                         'date': 'first'})
        plot_gdf.rename(columns={'likes': 'tweet_count'}, inplace=True)
        plot_gdf['lon'] = plot_gdf.geometry.x
        plot_gdf['lat'] = plot_gdf.geometry.y

        fig = px.scatter_geo(plot_gdf[['lat', 'lon', 'text', 'date', 'tweet_count', 'name']],
                             lat='lat', lon='lon', color="name", hover_name="name", size='tweet_count',
                             projection="natural earth")
        fig.show()

    def plot_tweets_heatmap(self, radius=20):
        self.compute_centroids()
        plot_gdf = self.tweets_centroid.dissolve(by='place_id', aggfunc={'name': 'first',
                                                                         'likes': 'count',
                                                                         'text': 'first',
                                                                         'date': 'first'})
        plot_gdf.rename(columns={'likes': 'tweet_count'}, inplace=True)
        plot_gdf['lon'] = plot_gdf.geometry.x
        plot_gdf['lat'] = plot_gdf.geometry.y

        fig = px.density_mapbox(plot_gdf, lat='lat', lon='lon', z='tweet_count', radius=radius,
                                center=dict(lat=0, lon=180), zoom=0,
                                mapbox_style="stamen-terrain")
        fig.show()

    def bubble_animation(self, time_unit='day'):
        self.compute_centroids()

        plot_gdf = self.tweets_centroid.copy()
        plot_gdf['lon'] = plot_gdf.geometry.x
        plot_gdf['lat'] = plot_gdf.geometry.y
        plot_gdf['year'] = plot_gdf.date.dt.year
        plot_gdf['month'] = plot_gdf.date.dt.month
        plot_gdf['day'] = plot_gdf.date.dt.day
        plot_gdf['hour'] = plot_gdf.date.dt.hour
        plot_gdf['minute'] = plot_gdf.date.dt.minute
        plot_gdf['second'] = plot_gdf.date.dt.second
        group_list_all = ['year', 'month', 'day', 'hour', 'minute', 'second']
        group_list_final = []

        for tunit in group_list_all:
            group_list_final.append(tunit)
            if tunit == time_unit:
                break
        agg_dict = {
            'country': 'first',
            'full_name': 'first',
            'place_id': 'count'
        }
        plot_gdf = plot_gdf.groupby(group_list_final + ['lat', 'lon']).agg(agg_dict).reset_index()
        plot_gdf.rename(columns={'place_id': 'tweet_count'}, inplace=True)
        plot_gdf['time'] = pd.to_datetime(plot_gdf[group_list_final]).dt.strftime('%m/%d/%Y %H:%M%:%S')

        fig = px.scatter_geo(plot_gdf, lat='lat', lon='lon', color="full_name",
                             hover_name="full_name", size='tweet_count',
                             animation_frame='time',
                             projection="natural earth")

        fig.layout.update(showlegend=False)
        fig.show()
