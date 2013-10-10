from datetime import datetime
import json

from tablib import Dataset
from unittest2 import TestCase

from capecommute import train


class TrainTestCase(TestCase):

    def test_parse_url(self):
        url = '_timetables/2013_04_08/South/ST_CT_Sun_April_2013.htm'
        self.assertEquals(
            ('South', 'ST', 'CT', 'Sun', datetime(2013, 4, 8, 0, 0)),
            train.parse_url(url)
        )

    def test_scrape_capemetro_urls(self):
        self.assertEquals(
            [
                ('http://www.capemetrorail.co.za/'
                 '_timetables/2013_04_08/Central/CT_KYL_MonFri_April_2013.htm'),
                ('http://www.capemetrorail.co.za/'
                 '_timetables/2013_04_08/Central/CT_KYL_Sat_April_2013.htm'),
            ],
            train.scrape_capemetro_urls()[:2]
        )

    def test_extract_station(self):
        row = ['SIMON`S TOWN', '04:24', '05:24', '06:22', '07:18', '08:17',
               '09:04', '09:55', '10:42', '11:53', 'SIMON`S TOWN', '13:00',
               '13:41', '14:54', '16:02']
        expected = list(set(row))
        expected.remove('SIMON`S TOWN')
        self.assertEquals(
            ('SIMON`S TOWN', sorted(expected)),
            train.extract_station(row)
        )

    def test_generate_dataset(self):
        station_times = {
            'Muizenberg': {
                'zone': 'South',
                'station': 'Muizenberg',
                'times': [{
                    '11:30': {
                        'train_number': '201',
                        'platform': '1',
                    }
                }]
            }
        }

        self.assertEquals(
            ('[{"zone": "South", "station": "Muizenberg", "time": "11:30", '
             '"train_number": "201", "platform": "1"}]'),
            train.generate_dataset(station_times).json
        )
