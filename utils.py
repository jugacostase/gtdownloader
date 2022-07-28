import ast
import numpy as np
from datetime import datetime

from shapely.geometry import Polygon


def get_attribute_id(x, attribute_id):
    try:
        return ast.literal_eval(x)[attribute_id]
    except ValueError:
        return np.nan


def get_attribute_from_dict(x, attribute_id):
    try:
        return x[attribute_id]
    except TypeError:
        return np.nan


def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%Sz')
        return date_text
    except ValueError:
        try:
            date_obj = datetime.strptime(date_text, '%m/%d/%Y %H:%M:%S')
        except ValueError:
            try:
                date_obj = datetime.strptime(date_text, '%m/%d/%Y')
            except ValueError:
                date_obj = datetime.strptime(date_text, '%m/%d/%Y %H:%M:')

        return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")


def extract_bbox_polygon(x):
    lon1 = x['bbox'][0]
    lat1 = x['bbox'][1]
    lon2 = x['bbox'][2]
    lat2 = x['bbox'][3]
    polygon = Polygon([(lon1, lat1), (lon1, lat2), (lon2, lat2), (lon2, lat1)])
    return polygon
