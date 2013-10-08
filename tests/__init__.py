from datetime import datetime

from tablib import Dataset
from unittest2 import TestCase

from capecommute import train, config


class TrainTestCase(TestCase):

    def test_parse_url(self):
        url = '_timetables/2013_04_08/South/ST_CT_Sun_April_2013.htm'
        self.assertEquals(
            ('South', 'ST', 'CT', 'Sun', datetime(2013, 4, 8, 0, 0)),
            train.parse_url(url)
        )

    def test_scrape_capemetro_urls(self):
        self.assertEquals(
            [#'%s/2013_04_08/South/ST_CT_Sun_April_2013.htm' % config.CAPEMETRO_URL,
             '%s/2013_09_06/South/CT_ST_MonFri_September_2013.htm' % config.CAPEMETRO_URL],
            train.scrape_capemetro_urls()
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

    # def test_append_to_dataset(self):
    #     original_data = Dataset()
    #     original_data.headers = ['first', 'second', 'third']

    #     row = [1, 2, 3]

    #     self.assertEquals(
    #         [dict(zip(original_data.headers, row))],
    #         train.append_to_dataset(original_data, row).dict
    #     )

    # def test_append_to_dataset_more_columns(self):
    #     original_data = Dataset()
    #     original_data.headers = ['first', 'second', 'third']

    #     row = [1, 2, 3, 4]

    #     self.assertEquals(
    #         [dict(zip(original_data.headers, row))],
    #         train.append_to_dataset(original_data, row).dict
    #     )

    def test_generate_dataset(self):
        pass
