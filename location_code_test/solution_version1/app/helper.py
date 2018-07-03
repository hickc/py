# TODO: possibly consider changing namedtuple to Py3.6+ typing.NamedTuple which includes type hints
import logbook
from collections import namedtuple 
from collections import OrderedDict 
import csv
import re
import sys
import random
import pprint


def calc_city_score(citydata_dict):
    log = logbook.Logger(__name__)
    log.info(f">>> calc_city_score(citydata_dict={pprint.pformat(citydata_dict)})")

    score = 0
    score += (10 - citydata_dict['crime_rate']) / 10 * 0.2
    score += citydata_dict['public_transport'] / 10 * 0.2
    weighted_avg_temp = (citydata_dict['current_temperature'] * 0.4 + citydata_dict['tomorrow_temperature'] * 0.6)
    if weighted_avg_temp >= 6 and weighted_avg_temp <= 32:
        score += 0.05
    if weighted_avg_temp >= 10 and weighted_avg_temp <= 28:
        score += 0.05
    if weighted_avg_temp >= 18 and weighted_avg_temp <= 26:
        score += 0.1
    if citydata_dict['average_hotel_cost'] <= 200:
        score += 0.1
    if citydata_dict['average_hotel_cost'] <= 140:
        score += 0.1
    if citydata_dict['current_weather_description'] in ['Light Cloud', 'Clear']:
        score += 0.2
    elif citydata_dict['current_weather_description'] in ['Heavy Cloud']:
        score += 0.1
    elif citydata_dict['current_weather_description'] in ['Light Rain']:
        score += 0.05
    ret = round(score*10,1)
    log.info(f"<<< calc_city_score() returns: {ret}")

    return ret
