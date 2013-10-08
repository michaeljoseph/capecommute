import logging

from datalogy.html import parse_html_table
import requests
import scraperwiki

from capecommute import train

log = logging.getLogger(__name__)


# TODO: cache html files etag
def main(debug=False):
    #
    logging.basicConfig(level='DEBUG' if debug else 'INFO')

    for url in train.scrape_capemetro_urls():
        try:
            zone, start_station, end_station, period, platforms, trains, station_times, parsed_timetable = (
                train.parse_timetable(url)
            )

            # dataset = train.generate_datasets(station_times, trains)

            table_name = (
                'capemetro_%s-%s-%s_train_schedule' %
                (zone, start_station, end_station)
            ).lower().replace('-', '_')

            log.debug('Saving table=%s', table_name)
            from pprint import pprint
            pprint(station_times, indent=4)

            # result = scraperwiki.sql.save([], dataset.dict, table_name=table_name)
            # log.info('scraperwiki.sql save result: %s', result)
        except:
            log.exception('%s bombed, continuing', url)
