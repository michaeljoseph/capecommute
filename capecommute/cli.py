import logging
import json

import scraperwiki

from capecommute import train

log = logging.getLogger(__name__)


# TODO: cache html files etag
def main(debug=False):
    #
    logging.basicConfig(level='DEBUG' if debug else 'INFO')

    # for url in [' http://www.capemetrorail.co.za/_timetables/2013_04_08/South/ST_CT_Sun_April_2013.htm']:#train.scrape_capemetro_urls():
    for url in ['http://www.capemetrorail.co.za/_timetables/2013_09_06/South/CT_ST_MonFri_September_2013.htm']:
        try:
            (zone, start_station, end_station, period, platforms, trains,
             stations, station_times) = train.parse_timetable(url)

            dataset = train.generate_dataset(station_times)

            table_name = (
                'capemetro_%s-%s-%s_train_schedule' %
                (zone, start_station, end_station)
            ).lower().replace('-', '_')

            log.debug('Saving table=%s', table_name)

            result = scraperwiki.sql.save(
                [],
                dataset.dict,
                table_name=table_name
            )
            log.info('scraperwiki.sql save result: %s', result)

            with open('%s.csv' % table_name, 'w') as csv_file:
                csv_file.write(dataset.csv)

            with open('%s.json' % table_name, 'w') as json_file:
                json_file.write(json.dumps(dataset.dict, indent=4))

        except:
            log.exception('%s bombed, continuing', url)
