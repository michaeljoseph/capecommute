import logging

import requests
import scraperwiki

from capecommute import config
from capecommute.train import parse_url, parse_html, generate_dataset

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level='DEBUG')
    cape_metro = config.CAPEMETRO_URL
    url = '%s/2013_04_08/South/ST_CT_Sun_April_2013.htm' % cape_metro

    zone, start_station, end_station, period = parse_url(url)
    log.info('Parsing timetable for '
             'zone=%s start_station=%s, end_station=%s, period=%s',
             zone, start_station, end_station, period
    )

    file_mask = '%s-%s-%s' % (zone, start_station, end_station)

    content = requests.get(url).content
    parsed_table = parse_html(content)
    log.info('Parsed %s rows', len(parsed_table))

    dataset = generate_dataset(parsed_table)
    log.info('Generated dataset %s', dataset)

    result = scraperwiki.sql.save(
        table.json.keys,
        table,
        'capemetro_%s_train_schedule' % file_mast
    )
    log.info('scraperwiki.sql save result: %s', result)

