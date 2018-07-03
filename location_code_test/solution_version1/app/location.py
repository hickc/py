import logbook

from app.helper import calc_city_score
from app.load_data import do_all_dataload_steps
from pathlib import Path
import app.cfg
import pprint

from app.weather import get_woeid, get_weather


def get_location(city):
    log = logbook.Logger(__name__)
    log.info(f">>> get_location(city={city})")
    if not(app.cfg.all_cities_data):
        app.cfg.all_cities_data = do_all_dataload_steps()
    #pprint.pprint(app.cfg.all_cities_data)

    citydata = app.cfg.all_cities_data.get('loaded_data').get(city)
    log.info(f"citydata: {citydata})")
    #print("~~~",citydata.current_temperature)
    #citydata.current_temperature = 123 #CH
    ret = {}
    if citydata:

        log.info(f"citydata retrieved from sample data citydata:{citydata}")

        ret = citydata._asdict()
        if app.cfg.LOAD_DATA_CONFIG['use_weather_api']:
            woeid = get_woeid(city)
            weather = get_weather(woeid)
            # ret['current_temperature'] = weather.get('current_temperature')
            # ret['tomorrow_temperature'] = weather.get('tomorrow_temperature')
            # ret['current_weather_description'] = weather.get('current_weather_description')
            # ret['humidity'] = weather.get('humidity')
            for k in ('current_temperature','tomorrow_temperature','current_weather_description','humidity'):
                ret[k] = weather.get(k)

            log.info(f"After weather api update ret:{ret}")

        city_score = calc_city_score(ret)
        log.info(f"city_score:{city_score}")


        ret['city_score'] = city_score
        # Remove 'index' from dict as it is not required
        if 'index' in ret:
            del ret['index']
    log.info(f"<<< get_location() returns: {ret}")
    return ret

