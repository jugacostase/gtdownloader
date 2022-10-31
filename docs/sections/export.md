## Exporting results

There are two main ways to deal with the downloaded data for further processing: by exporting tabular data and exporting shapefiles.

### Tabular data
`GTdownloader` stores dataframes making use of the `pandas.DataFrame()`. Hence, all the pandas exporting functions are available for usage, such as `pandas.DataFrame.to_csv` and `pandas.DataFrame.to_excel`.

For instance, after running the `get_tweets()` function you can save the results to csv files by accessing the corresponfing class attributes and calling the `to_csv` method in the following way:
```python
# exporting tweets as a csv file in the downloads folder
gtd.tweets_df.to_csv('downloads/my_downloaded_tweets.csv')

# exporting places as a csv file in the downloads folder
gtd.places_df.to_csv('downloads/my_downloaded_tweet_locations.csv')

# exporting authors as a csv file in the downloads folder
gtd.authors_df.to_csv('downloads/my_downloaded_tweets_authors.csv')
```

### Shapefile

To export data with its corresponding geographical information there are two main options: exporting bounding boxes and exporting centroids. The default geographical object returned by the Twitter API is a bounding box. Its size will be given by the available location precision. Since most geographical analysis and visualization require point pattern data, you can algo download the corresponding centroids. However, we recommend you proceed carefully and always verify whether a point is representing a city or an entire country in the attributes table. 

```python
# exporting tweets centroids as shapefile in the downloads folder
gtd.tweets_to_shp(save_path='downloads', geo_type='centroids')

# exporting tweets bounding boxes as shapefile in the downloads folder
gtd.tweets_to_shp(save_path='downloads', geo_type='bbox')


```
