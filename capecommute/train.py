from datetime import datetime
import logging

from datalogy.html import (
    clean_table, pad_list, non_empty, remove_nbsp,
    strip_unprintables, normalise_tabular_labelling
)
import tablib

from capecommute import config

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


def scrape_capemetro_urls():
    # urls = []
    # '%s/Timetables.html' % config.CAPEMETRO_URL
    # content = requests.get(url).content
    # for link in
    return [
        # '%s/2013_04_08/South/ST_CT_Sun_April_2013.htm' % config.CAPEMETRO_URL,
        '%s/2013_09_06/South/CT_ST_MonFri_September_2013.htm' % config.CAPEMETRO_URL
    ]


def extract_station(row):
    """The first column has the station name"""
    station = row.pop(0)
    row = normalise_tabular_labelling(row, station)
    return station, sorted(row)


def resized_row(row, length):
    row_needs_padding = length < len(row)
    new_column_length = max(len(row), length)

    log.debug('resized_row row=%s', row)
    if row_needs_padding:
        return new_column_length, pad_list(row, length)

    return new_column_length, row


def generate_dataset(table, headers):
    data = tablib.Dataset()
    data.headers = headers
    for row in table:
        data.append(row)
    return data


def parse_timetable(table):
    row_data = clean_table(table)

    heading = row_data.pop()
    platforms = row_data.pop()

    column_length = len(heading) 
    station_times = {}

    parsed_table = []
    for row in row_data:
        station = row.pop(0)
        if non_empty(row):
            column_length, row = resized_row(row, column_length)
        log.debug('Processing station %s', station)
        station_times[station] = [
            ''
        ]
        parsed_table.append(row)

    trains = station_times.keys()
    return platforms, trains, station_times, parsed_table 


