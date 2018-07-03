import logbook
import requests
from http import HTTPStatus
from collections import namedtuple
from collections import OrderedDict 
import csv
import re
import sys
import random
import pprint
import json

import app.cfg

_woeid_cache = {}

def get_woeid(city):
    log = logbook.Logger(__name__)
    log.info(f">>> get_woeid(city={city})")

    woeid = _woeid_cache.get(city)
    if not(woeid):
        woeid = _get_woeid(city)
        if woeid and app.cfg.LOAD_DATA_CONFIG['weather_api_cache_woeid']:
            _woeid_cache[city] = woeid
    else:
        log.info("woeid retrieved from cache")
    log.info(f"<<< get_woeid() returns: {woeid}")
    return woeid


def _get_woeid(city):
    log = logbook.Logger(__name__)
    log.info(f">>> _get_woeid(city={city})")
    woeid = None
    #city = 'london' # test city with space in name
    try:
        resp = requests.get(f'https://www.metaweather.com/api/api/location/search/?query={city}')


        #print(resp.status_code)
        #print(resp.headers)
        #print(resp.text)
        #print(resp.json())

        if resp.status_code != HTTPStatus.OK:
            raise Exception

        resp_json = resp.json()
        if len(resp_json)==0:
            raise Exception
        if resp_json[0].get('title').lower()!=city:
            raise Exception

        woeid = resp_json[0].get('woeid')
        woeid = int(woeid)

    except requests.exceptions.ConnectionError as ex:
        log.error(f'ConnectionError {ex}')
        #raise Exception
    except Exception as ex:
        log.error(f'ConnectionError {ex}')
        #raise Exception

    log.info(f"<<< _get_woeid() returns: {woeid}")
    return woeid
    
def get_weather(woeid):
    log = logbook.Logger(__name__)
    log.info(f">>> get_weather(woeid={woeid})")

    resp = requests.get(f'https://www.metaweather.com/api/api/location/{woeid}')
    if resp.status_code != HTTPStatus.OK:
        raise Exception

    #print(resp.status_code)
    #print(resp.headers)
    #print(resp.text)
    #print(resp.json())
    resp_json = resp.json()
    weather = resp_json.get('consolidated_weather')
    if len(weather) < 2:
        raise Exception
    current_temperature = weather[0].get('the_temp')
    humidity = weather[0].get('humidity')
    current_weather_description = weather[0].get('weather_state_name')
    tomorrow_temperature = weather[1].get('the_temp')
    #print(temp_today)
    #print(humidity)
    #print(weather_desc)
    #print(temp_tomorrow)
    ret = {'current_temperature':current_temperature, 'humidity':humidity, 'current_weather_description':current_weather_description, 'tomorrow_temperature':tomorrow_temperature}
    log.info(f"<<< get_weather() returns: {ret}")
    return ret





