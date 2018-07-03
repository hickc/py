import sys
from pathlib import Path

import logbook

import tornado.ioloop
import tornado.web

# import app.load_data
#import app.location
from app.helper import calc_city_score
from app.load_data import do_all_dataload_steps
from app.location_comparison_handler import LocationComparisonHandler
from app.location_data_handler import LocationHandler
from app.weather import get_woeid, get_weather
import app.cfg

log_name = 'location_api'


def logging_init(logfile=None):
    if logfile:
        logbook.TimedRotatingFileHandler(
            logfile, level=logbook.INFO, date_format='%Y-%m-%d').push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=logbook.INFO).push_application()


def make_app():
    return tornado.web.Application([(r"/location-data/([a-zA-Z0-9]*)?", LocationHandler, {}),
                                    (r"/location-comparison/cities=\[(\S+)\]", LocationComparisonHandler, {})])


if __name__ == "__main__":
    assert sys.version_info >= (3, 6)

    # logging_init("location_api.log")
    logging_init()
    log = logbook.Logger(__name__)
    log.info('location_api REST server starting')

    app.cfg.root_fullpath = Path('.').absolute().as_posix()
    log.info(f'app.cfg.root_fullpath: {app.cfg.root_fullpath}')


    do_all_dataload_steps()

    calc_city_score(app.cfg.all_cities_data['loaded_data'].get('dublin')._asdict())

    city = 'dublin'
    woeid = get_woeid(city)
    # print(woeid)

    weather = get_weather(woeid)
    # print(weather)
    # print()
    # pprint.pprint(weather)

    application = make_app()
    port = 8484
    application.listen(port)
    log.info(f'location_api REST server event loop about to listen on port {port}')
    tornado.ioloop.IOLoop.current().start()
