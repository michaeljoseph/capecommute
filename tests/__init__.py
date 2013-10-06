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
