from datetime import datetime
import logging

from datalogy.html import (
    clean_table, pad_list, non_empty, remove_nbsp,
    strip_unprintables, normalise_tabular_labelling
)
import tablib

log = logging.getLogger(__name__)


def parse_url(url):
    path_components = url.split('/')
    date, zone, title = path_components[-3:]
    (start_station, end_station, period) = title.split('_')[:3]

    return (
        zone,
        start_station, end_station,
        period,
        datetime.strptime(date, '%Y_%m_%d')
    )




def extract_station(row):
    """The first column has the station name"""
    data = tablib.Dataset()

    stations = []

    return data
