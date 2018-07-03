"""
Version 1 of Cities REST API application supports the following sample requests
    http://127.0.0.1:8484/location-data/dublin
    http://127.0.0.1:8484/location-comparison/cities=[dublin,London,Copenhagen]
and will work for all rows loaded from european_cities.csv
(some rows are not loaded as they fail validation which is shown in startup logs).

This version does not include thew following which will be included in the next version
1: UnitTesting and interface tests using Pytest.
2: This version is blocking, i.e. synchronous.  This app could handle more requests if
    it is changed to async.  An async non blocking versoin should be simple to implementat
     using yield and @tornado.web.asynchronous, @tornado.gen.engine decorators in handler methods.
     Perhaps include some load testing @tornado.gen.engine with Locust tooling to show benefit of switch to async.
3: Better exception handling
4: Docstrings on all modules, functions/methods.
5: Some refactoring. Revisit use of mix of immutable namedtuple and dicts to store city data.
    A mutable class may be more appropriate.
    Better decoupling of inclusion of csv test data or not using stubs, monkey patching or whatever.
"""

LOAD_DATA_CONFIG = {
    'csv_filename_to_load': 'data/european_cities.csv',

    # if not set or ecaluates false, then this optional output csv will not be generated
    'csv_filename_loaded_data': 'data/european_cities_TIDIED_AND_AUGMENTED.csv',

    #If True get weather from www.metaweather.com, if False use weather in sample data file
    'use_weather_api': False,

    # Use caching of woeid values from previous weather API requests
    'weather_api_cache_woeid': True,
}

# The following variables are shared throughout the application
root_fullpath = None  # Full path to where application is started
all_cities_data = None  # Contains all sample citydata from loaded csv file