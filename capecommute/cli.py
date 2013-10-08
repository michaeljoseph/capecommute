import logging

from datalogy import html
import requests
import scraperwiki

from capecommute import train

log = logging.getLogger(__name__)


# TODO: cache html files etag
def main():
    logging.basicConfig(level='DEBUG')

    for url in train.scrape_capemetro_urls():
        zone, start_station, end_station, period, timetable_date = train.parse_url(url)
        log.info(
            'Parsing timetable for '
            'zone=%s start_station=%s, end_station=%s, period=%s, date=%s',
            zone, start_station, end_station, period, timetable_date
        )

        table_name = (
            'capemetro_%s-%s-%s_train_schedule' %
            (zone, start_station, end_station)
        ).lower()

        content = requests.get(url).content
        parsed_html_table = html.parse_html_table(content)[::-1]
        log.info('Parsed %s rows', len(parsed_html_table))

        platforms, trains, station_times, parsed_timetable = train.parse_timetable(parsed_html_table)

        dataset = train.generate_dataset(parsed_timetable, platforms)
        log.debug('Saving data=%s, table=%s',
                  dataset.dict,
                  table_name)

        result = scraperwiki.sql.save([], dataset.dict)
        log.info('scraperwiki.sql save result: %s', result)
