import pprint

import logbook
from tornado.web import RequestHandler
from http import HTTPStatus
import json

import app.cfg



class LocationHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        """
        Retrieve information about a city.
        :param args:
        :param kwargs:
        :return:
        """

        log = logbook.Logger(__name__)
        log.info(f">>> get(args={args},kwargs={kwargs})")

        city = args[0]
        city = city.lower()
        response = app.location.get_location(city)
        #print(type(response))
        #pprint.pprint(response)


        """
        response = {'city_name': 'faketown',
                    'current_temperature': 32.2,
                    'current_weather_description': 'Cloudy',
                    'population': 123456,
                    'bars': 654321,
                    'city_score': 6.8}
        """

        self.set_status(HTTPStatus.OK)
        self.write(json.dumps(response))
        log.info(f"<<< get()")

