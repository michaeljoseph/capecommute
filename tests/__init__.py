from unittest2 import TestCase

from capecommute import train

class TrainTestCase(TestCase):

    def test_parse_url(self):
        url = '_timetables/2013_04_08/South/ST_CT_Sun_April_2013.htm'
        self.assertEquals(
            ('South', 'ST', 'CT', 'Sun'),
            train.parse_url(url)
        )

    def test_parse_html(self):
        html = '<html></html>'
        expected = []
        self.assertTrue(
            isinstance(train.parse_html(html), list)
        )

    def test_pad_list(self):
        row = [1, 2, 3]
        self.assertEquals(
            row + [None],
            train.pad_list(row, 4)
        )

    def test_pad_list_right_size(self):
        row = [1, 2, 3]
        self.assertEquals(
            row,
            train.pad_list(row, 3)
        )

