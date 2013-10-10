from datetime import datetime
import logging

from datalogy import html, util
from pyquery import PyQuery as pq
import requests
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
    content = requests.get('%s/Timetables.html' % config.CAPEMETRO_URL).content

    urls = []
    for link in pq(content)('a'):
        href = link.attrib['href']
        if '_timetables/' in href and 'htm' in href:
            urls.append('%s/%s' % (config.CAPEMETRO_URL, href))
    return urls


def extract_station(row):
    """The first column has the station name"""
    station = row.pop(0)
    row = html.normalise_tabular_labelling(row, station)
    return station, sorted(row)


def resized_row(row, length):
    row_needs_padding = length < len(row)
    new_column_length = max(len(row), length)

    if row_needs_padding:
        return (
            new_column_length,
            util.pad_list(row, length, missing_value='N/A')
        )

    return new_column_length, row


def generate_dataset(station_times):
    dataset = tablib.Dataset()
    dataset.headers = [
        'zone', 'station', 'time', 'train_number', 'platform'
    ]

    for station, data in station_times.items():
        for times in data['times']:
            for time, time_data in times.items():
                dataset.append((
                    data['zone'],
                    station,
                    time,
                    time_data['train_number'],
                    time_data['platform']
                ))
    return dataset


def parse_train_numbers(table):
    train_numbers = table.pop(0)[1:]
    log.debug('Train Numbers: %s', train_numbers)
    return train_numbers


def parse_platform_numbers(table):
    # first cell is the heading
    platforms = table.pop(0)[:]
    for index, platform in enumerate(platforms):
        if not (platform and platform.isdigit()):
            del platforms[index]

    log.debug('Platforms: %s', platforms)
    return platforms


def parse_stations(table):
    stations = []
    for row in table:
        if row and isinstance(row[0], basestring) and row[0].isupper():
            stations.append(row[0])
    log.debug('Stations: %s', stations)
    return stations


def generate_time_list(row, lookup_train_number, lookup_platform_number):
    time_list = []
    # usual platform
    row.pop(0)
    log.info('times: %s', row)

    for index, time in enumerate(row):
        # if time:
        time_list.append({
            time: {
                'train_number': util.get_default(lookup_train_number, index-1),
                'platform': util.get_default(lookup_platform_number, index-1),
            }
        })
    return time_list


def parse_timetable(url):

    table = html.parse_html_table(
        requests.get(url).content
    )
    log.info('Parsed %s rows', len(table))

    zone, start_station, end_station, period, timetable_date = parse_url(url)
    log.info(
        'Parsing timetable for '
        'zone=%s start_station=%s, end_station=%s, period=%s, date=%s',
        zone, start_station, end_station, period, timetable_date
    )

    table = html.clean_table(table)

    platforms = parse_platform_numbers(table)
    train_numbers = parse_train_numbers(table)
    stations = parse_stations(table)
    column_length = len(train_numbers)
    station_times = {}

    for row in table:
        # if is alpha and isupper
        station = row.pop(0)

        if util.non_empty(row):
            column_length, times = resized_row(row, column_length)
        log.debug('Processing station %s', station)

        station_times[station] = {
            'zone': zone,
            'start_station': start_station,
            'end_station': end_station,
            'period': period,
            'direction': 'direction',
            'times': generate_time_list(row, train_numbers, platforms),
        }

    trains = station_times.keys()

    return (zone, start_station, end_station, period, platforms, trains,
            stations, station_times)
