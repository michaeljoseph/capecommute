#!/usr/bin/env python

import logging

from pyquery import PyQuery as pq
import requests
import tablib
import scraperwiki

log = logging.getLogger(__name__)


def parse_url(url):
    path_components = url.split('/')
    date, zone, title = path_components[-3:]
    (start_station, end_station, period) = title.split('_')[:3]
    return zone, start_station, end_station, period


def store_timetable(keys, data, table_name):
    return scraperwiki.sql.save(keys, data, table_name=table_name)


def parse_html(html):
    html_table = []
    document = pq(html)
    for row in document('table > tr'):
        row_data = []
        for cell in row.iterchildren():
            row_data.append(cell.text_content())
        html_table.append(row_data)
    return html_table


def pad_list(row, length):
    if len(row) < length:
        return row + [length-len(row) * None]


def generate_dataset():
    data = tablib.Dataset()
    data.headers = ('name', 'age')
    return data


def serve_output_type(datatable, output_type):
    # output_types = ['csv', 'json']
#        with open('%s.%s' % (file_mask, output_type), 'w') as filename:
    return datatable.output_type()


def main():
    cape_metro = 'http://www.capemetrorail.co.za/_timetables'
    url = '%s/2013_04_08/South/ST_CT_Sun_April_2013.htm' % cape_metro

    print(parse_url(url))

    zone, start_station, end_station, period = parse_url(url)
    file_mask = '%s-%s-%s' % (zone, start_station, end_station)

    content = requests.get(url).content
    table = parse_html(content)
    print('Parsed %s rows' % len(table))
    #store_timetable(table.json.keys(), table, 'capemetro_%s_train_schedule'))

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    main()
