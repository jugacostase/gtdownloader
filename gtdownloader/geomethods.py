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
        self.output_folder = downloader.output_folder

    def create_gdf(self):
        # Create Polygon from bboxes in the places dataframe before creating geodataframe
        try:
            self.places_df['geometry'] = self.places_df['geo'].apply(extract_bbox_polygon)
        except KeyError:
            self.places_df['geometry'] = np.nan
        self.places_bbox = gpd.GeoDataFrame(self.places_df, crs="EPSG:4326")
        self.places_bbox.rename(columns={'id': 'place_id'}, inplace=True)

    def get_tweets_gdf(self, geo_type='centroids'):
        self.tweets_df.rename(columns={'id': 'tweet_id'}, inplace=True)
        try:
            self.tweets_df.drop(columns=['edit_history_tweet_ids'], inplace=True)
        except:
            pass
        if geo_type == 'centroids':
            self.compute_centroids()
            #shape_filename = os.path.join(os.getcwd(), save_path, self.filename + '_tweets_centroids' + '.shp')
            tweets_centroid = self.tweets_centroid
            tweets_centroid['date'] = tweets_centroid.date.dt.strftime('%m/%d/%Y %H:%M%:%s')
            tweets_centroid.drop(columns=['public_metrics', 'created_at'], inplace=True)
            tweets_centroid.rename(columns={'country_code': 'cntry_code',
                                            'conversation_id': 'conv_id',
                                            'name': 'place',
                                            'full_name': 'full_place'}, inplace=True)
            return tweets_centroid
            #tweets_centroid.to_file(shape_filename)
            #print('Shapefile with tweet centroids saved to file:', shape_filename)
        elif geo_type == 'bbox':
            try:
                self.tweets_bbox = pd.merge(self.places_bbox, self.tweets_df, on='place_id')
                self.tweets_bbox.drop(columns=['geo_x', 'geo_y'])
                self.tweets_bbox.rename(columns={'id': 'place_id'}, inplace=True)
                tweets_bbox = self.tweets_bbox
                tweets_bbox['date'] = tweets_bbox.date.dt.strftime('%m/%d/%Y %H:%M%:%s')
                tweets_bbox.rename(columns={'country_code': 'cntry_code',
                                            'conversation_id': 'conv_id',
                                            'name': 'place',
                                            'full_name': 'full_place'}, inplace=True)
            except:
                self.tweets_bbox = gpd.GeoDataFrame(self.tweets_df)
                tweets_bbox = self.tweets_bbox
                tweets_bbox['geometry'] = np.nan
            return tweets_bbox
            #shape_filename = os.path.join(save_path, self.filename + '_tweets_bboxes' + '.shp')
            #tweets_bbox.to_file(shape_filename)
            #print('Shapefile with tweet bounding boxes saved to file:', shape_filename)
        else:
            raise ValueError('geo_type not supported. Input either "centroids" or "bbox"')

    def get_places_gdf(self, geo_type='centroids'):
        if geo_type == 'centroids':
            self.compute_centroids()
            #shape_filename = os.path.join(save_path, self.filename + '_places_centroids' + '.shp')
            return self.places_centroid
            #self.places_centroid.to_file(shape_filename)
            #print('Shapefile with places centroids saved to file:', shape_filename)
        elif geo_type == 'bbox':
            return self.places_bbox
            #shape_filename = os.path.join(save_path, self.filename + '_places_bboxes' + '.shp')
            #self.places_bbox.to_file(shape_filename)
            #print('Shapefile with places bounding boxes saved to file:', shape_filename)
        else:
            raise ValueError('geo_type not supported. Input either "centroids" or "bbox"')

    def compute_centroids(self):
        self.places_centroid = self.places_bbox.copy()
        self.places_centroid['geometry'] = self.places_centroid.to_crs("EPSG:3395").geometry.centroid
        self.places_centroid = self.places_centroid.to_crs("EPSG:4326")
        self.places_centroid.rename(columns={'id': 'place_id'}, inplace=True)
        try:
            self.tweets_centroid = pd.merge(self.places_centroid, self.tweets_df, on='place_id')
            self.tweets_centroid.drop(columns=['geo_x', 'geo_y'], inplace=True)
        except KeyError:
            #self.places_centroid = gpd.GeoDataFrame(self.places_df)
            self.tweets_centroid = gpd.GeoDataFrame(self.tweets_df)
            self.tweets_centroid['geometry'] = np.nan


    def simple_tweets_map(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        base = world.plot(color='white', edgecolor='black')
        self.compute_centroids()
        self.tweets_centroid.plot(ax=base, marker='o', color='red', markersize=5)
        plot_filename = os.path.join(self.output_folder, self.filename + '_simple_map.png')
        plt.savefig(plot_filename)
        plt.show(block=False)

    def plot_tweets_points(self):

        self.compute_centroids()
        plot_gdf = self.tweets_centroid
        plot_gdf['lon'] = plot_gdf.geometry.x
        plot_gdf['lat'] = plot_gdf.geometry.y

        print(plot_gdf.columns)
        plot_gdf.sort_values('likes', ascending=False, inplace=True)
        agg_dict = {
            'country': 'first',
            'full_name': 'first',
            'place_id': 'count',
            'text': 'first',
            'date': 'first',
            'likes': 'first',
            'name': 'first'
        }

        plot_gdf = plot_gdf.groupby(['lat', 'lon']).agg(agg_dict).reset_index()
        plot_gdf.rename(columns={'name': 'place'}, inplace=True)

        fig = px.scatter_geo(plot_gdf[['lat', 'lon', 'text', 'date', 'likes', 'place']],
                             lat='lat', lon='lon', color="place", hover_name="text",
                             projection="natural earth")
        fig.layout.update(showlegend=False)
        plot_filename = os.path.join(self.output_folder, self.filename + '_tweet_points.html')
        fig.write_html(plot_filename)
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
        fig.layout.update(showlegend=False)
        plot_filename = os.path.join(self.output_folder, self.filename + '_tweet_points_aggr.html')
        fig.write_html(plot_filename)
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
        plot_filename = os.path.join(self.output_folder, self.filename + '_heatmap.html')
        fig.write_html(plot_filename)
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

        if 'day' in group_list_final:
            plot_gdf['time'] = pd.to_datetime(plot_gdf[group_list_final]).dt.strftime('%m/%d/%Y %H:%M%:%S')

            fig = px.scatter_geo(plot_gdf, lat='lat', lon='lon', color="full_name",
                                 hover_name="full_name", size='tweet_count',
                                 animation_frame='time',
                                 projection="natural earth")
        elif 'month' in group_list_final:
            plot_gdf['day'] = '1'
            plot_gdf['time'] = pd.to_datetime(plot_gdf[group_list_final+['day']]).dt.strftime('%m/%d/%Y %H:%M%:%S')

            fig = px.scatter_geo(plot_gdf, lat='lat', lon='lon', color="full_name",
                                 hover_name="full_name", size='tweet_count',
                                 animation_frame='time',
                                 projection="natural earth")
        else:
            fig = px.scatter_geo(plot_gdf, lat='lat', lon='lon', color="full_name",
                                 hover_name="full_name", size='tweet_count',
                                 animation_frame='year',
                                 projection="natural earth")

        fig.layout.update(showlegend=False)
        plot_filename = os.path.join(self.output_folder, self.filename + '_map_animation.html')
        fig.write_html(plot_filename)
        fig.show()
