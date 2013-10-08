import logging

import requests
import scraperwiki

from capecommute import config
from capecommute.train import parse_url, parse_html_table, generate_dataset

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level='DEBUG')

    for url in train.scrape_capemetro_urls():
        zone, start_station, end_station, period, timetable_date = train.parse_url(url)
        log.info(
            'Parsing timetable for '
            'zone=%s start_station=%s, end_station=%s, period=%s, date=%s',
            zone, start_station, end_station, period, timetable_date
        )

        table_name = 'capemetro_%s-%s-%s_train_schedule' % (zone, start_station, end_station)

        content = requests.get(url).content
        parsed_table = html.parse_html_table(content)
        log.info('Parsed %s rows', len(parsed_table))

        dataset = train.generate_dataset(parsed_table)
        log.debug('Generated dataset %s', dataset.dict)

        import pprint
        pprint.pprint(dataset.dict)
        log.debug('Saving data=%s, table=%s',
                  dataset.dict,
                  table_name)

        result = scraperwiki.sql.save([], dataset.dict)
        log.info('scraperwiki.sql save result: %s', result)
