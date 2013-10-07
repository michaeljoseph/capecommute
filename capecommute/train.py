#!/usr/bin/env python
from datetime import datetime

import logging

from pyquery import PyQuery as pq
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


# TODO: move to datalogy
# scrape(html, expression)
def parse_html(html):
    html_table = []
    document = pq(html)
    for row in document('table > tr'):
        row_data = []
        for cell in row.iterchildren():
            row_data.append(cell.text_content())
        html_table.append(row_data)
    return html_table


# TODO: move to datalogy
def pad_list(row, length):
    padding = length - len(row)
    if padding:
        padding = padding * [None]
        return row + padding
    return row


# TODO: move to datalogy
def non_empty(row):
    return any([cell for cell in row])


def normalise_tabular_labelling(row, marker_item):
    for item in row:
        if item == marker_item:
            row.remove(item)
    return row


def extract_station(row):
    """The first column has the station name"""
    return row[0]


def generate_dataset(parsed_html):
    data = tablib.Dataset()
    headers = []
    while not headers:
        # first (non-empty) row is the train numbers
        header_row = parsed_html.pop()
        if non_empty(header_row):
            headers = header_row
    data.headers = headers

    stations = []
    # TODO: write a function for each transformation
    for row_data in parsed_html:
        stations.append(extract_station(row_data))
        data.append(pad_list(row_data, data.width))

    return data
