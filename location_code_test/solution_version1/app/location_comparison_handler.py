import logbook
from tornado.web import RequestHandler
from http import HTTPStatus
import json

import app
from app.location import get_location


class LocationComparisonHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        """
        Retrieves information about multiple cities, rates them and returns a ranking and score for each city.
        :param args:
        :param kwargs:
        :return:
        """

        log = logbook.Logger(__name__)
        log.info(f">>> get(args={args},kwargs={kwargs})")

        cities = args[0].lower().split(',')
        rank_arr = []
        for city in cities:
            response = get_location(city)
            if response:
                rank_arr.append({'city_name':city,'city_score':response['city_score']})
        print('rank_arr:',rank_arr)

        rank_arr = sorted(rank_arr, key=lambda k: k['city_score'])
        for i,d in enumerate(rank_arr):
            d['city_rank'] = i+1

        response = {'city_data':rank_arr}

        """
        response = {'city_data': [{'city_name': 'greatplace',
                                   'city_rank': 1,
                                   'city_score': 8.4},
                                  {'city_name': 'okplace',
                                   'city_rank': 2,
                                   'city_score': 5.2},
                                  {'city_name': 'badplace',
                                   'city_rank': 3,
                                   'city_score': 2.2}
                                  ]}
        """

        self.set_status(HTTPStatus.OK)
        self.write(json.dumps(response))
        log.info(f"<<< get()")
