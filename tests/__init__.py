from datetime import datetime

from unittest2 import TestCase

from capecommute import train


class TrainTestCase(TestCase):

    row = [1, 2, 3]

    def test_parse_url(self):
        url = '_timetables/2013_04_08/South/ST_CT_Sun_April_2013.htm'
        self.assertEquals(
            ('South', 'ST', 'CT', 'Sun', datetime(2013, 4, 8, 0, 0)),
            train.parse_url(url)
        )

    def test_parse_html(self):
        html = '<html></html>'
        self.assertTrue(
            isinstance(train.parse_html(html), list)
        )

    def test_pad_list(self):
        self.assertEquals(
            self.row + [None],
            train.pad_list(self.row, 4)
        )

    def test_pad_list_right_size(self):
        self.assertEquals(
            self.row,
            train.pad_list(self.row, 3)
        )

    def test_non_empty(self):
        self.assertTrue(train.non_empty(self.row))
        self.assertFalse(train.non_empty(['', None]))

    def test_extract_stations(self):
        pass

    def test_extract_train_numbers(self):
        pass

    def test_generate_dataset(self):
        pass
