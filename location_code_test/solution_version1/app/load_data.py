import pathlib

import logbook
from collections import namedtuple
from collections import OrderedDict
import csv
import re
import sys
import os
import random
import pprint

#import app.location
import app.cfg

NUM_COLUMNS = 9
COL_OFFSET = 1
ROW_OFFSET = 2


class InputDataCSVFileNotConfiguredError(ValueError):
    pass


class CityColumnNotInCSVError(ValueError):
    pass


class InvalidNumColumnsError(ValueError):
    pass


class StrNotAlphaSpaceError(ValueError):
    pass


class ValueLessThanEqual0Error(ValueError):
    pass


class DuplicateCityError(ValueError):
    pass


def _tidy_str_column(s):
    log = logbook.Logger(__name__)
    log.trace(f">>> _tidy_str_column(s='{s}')")
    s_tidied = str(s).strip().lower().replace('-', ' ').replace('/', ' ').replace(' & ', ' and ')
    # Check that chars are all alpha or space.  
    # Regex not complex enough to warrant verbose regex syntax.
    if not (re.match(r'^[a-z ]+$', s_tidied)):
        raise StrNotAlphaSpaceError
    log.trace(f"<<< _tidy_str_column() returns: {s_tidied}")
    return s_tidied


def load_city_csv(csv_filename):
    log = logbook.Logger(__name__)
    log.info(f">>> load_city_csv(csv_filename='{csv_filename}')")

    # assert os.path.exists(csv_filename),f'CSV input file {csv_filename} not found'
    assert pathlib.Path.exists(pathlib.Path(csv_filename)), f'CSV input file {csv_filename} not found'

    with open(csv_filename) as f:
        reader = csv.reader(f)
        col_names = next(reader)
        try:
            col_names[col_names.index('city')] = 'city_name'
        except:
            raise CityColumnNotInCSVError
        CityDataNarrow = namedtuple("CityDataNarrow", col_names)
        num_input_rows = 0
        data = OrderedDict()
        for i, r in enumerate(reader):
            num_input_rows += 1
            r_mod = r
            try:
                num_columns = len(r_mod)
                # If 2nd column contain '?' consider it to be a ',' column seperator,
                # and resolve by spliting on '?' if present and adjusting r_mod
                if num_columns == (NUM_COLUMNS - 1):
                    r_mod[1:2] = r_mod[1].split('?')
                    num_columns = len(r_mod)
                if num_columns != NUM_COLUMNS:
                    raise InvalidNumColumnsError
                for ix, item in enumerate(r_mod):
                    if ix in (1, 2):
                        r_mod[ix] = _tidy_str_column(item)
                    else:
                        r_mod[ix] = int(item)
                        if r_mod[ix] <= 0:
                            raise ValueLessThanEqual0Error
                d = CityDataNarrow(*r_mod)
                if data.get(d.city_name):
                    raise DuplicateCityError
                data[d.city_name] = d
            except StrNotAlphaSpaceError as ex:
                log.warning(
                    f'DATA ROW FAILS VALIDATION AND IS BEING IGNORED. {r_mod[ix]} should be alpha or space in column {ix+COL_OFFSET}.  Line {i+ROW_OFFSET} with row contents {r_mod}.  {ex}')
            except InvalidNumColumnsError as ex:
                log.warning(
                    f'DATA ROW FAILS VALIDATION AND IS BEING IGNORED. Row has invalid num columns {num_columns} instead of {NUM_COLUMNS} expected.  Line {i+ROW_OFFSET} with row contents {r_mod}. {ex}')
            except ValueLessThanEqual0Error as ex:
                log.warning(
                    f'DATA ROW FAILS VALIDATION AND IS BEING IGNORED. {r_mod[ix]} has value <= 0 in column {ix+COL_OFFSET}.  Line {i+ROW_OFFSET} with row contents {r_mod}.  {ex}')
            except DuplicateCityError as ex:
                log.warning(
                    f'DATA ROW FAILS VALIDATION AND IS BEING IGNORED. Row contains a city that is present earlier in input.  Line {i+ROW_OFFSET} with row contents {r_mod}.  {ex}')
            except ValueError as ex:
                log.warning(
                    f'DATA ROW FAILS VALIDATION AND IS BEING IGNORED. {r_mod[ix]} cannot be converted to expected type for column {col_names[ix]} in column {ix+COL_OFFSET}.  Line {i+ROW_OFFSET} with row contents {r_mod}.  {ex}')

    # pprint.pprint(data)
    ret = {'loaded_data': data, 'num_input_rows': num_input_rows, 'num_rows_invalid_format': num_input_rows - len(data)}
    log.info(f"<<< load_city_csv() returns: {pprint.pformat(ret)}")
    return ret


def write_city_csv(citydata, file):
    log = logbook.Logger(__name__)
    log.info(f">>> write_city_csv(citydata={pprint.pformat(citydata)},file={file})")
    # pprint.pprint(data)
    # data['berlin']

    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ''
        for k, v in citydata.items():
            if not (header):
                header = v._fields
                writer.writerow(header)
            writer.writerow(v)
    log.info(f"<<< write_city_csv()")


def augment_city_data(citydata_narrow):
    log = logbook.Logger(__name__)
    log.info(f">>> augment_city_data(citydata_narrow={pprint.pformat(citydata_narrow)})")

    num_cities = len(citydata_narrow)

    new_cols = []

    random.seed(1)
    current_temperature = [round(random.uniform(-3, 38), 2) for _ in range(len(citydata_narrow))]
    new_cols.append('current_temperature')

    random.seed(2)
    tomorrow_temperature = [round(random.uniform(-3, 38), 2) for _ in range(len(citydata_narrow))]
    new_cols.append('tomorrow_temperature')

    random.seed(3)
    humidity = [round(random.uniform(60, 90)) for _ in range(len(citydata_narrow))]
    new_cols.append('humidity')

    random.seed(4)
    current_weather_description = [random.choice(
        ['Snow', 'Sleet', 'Hail', 'Thunderstorm', 'Heavy Rain', 'Light Rain', 'Showers', 'Heavy Cloud', 'Light Cloud',
         'Clear']) for _ in range(len(citydata_narrow))]
    new_cols.append('current_weather_description')

    existing_cols = citydata_narrow.get(next(iter(citydata_narrow)))._fields

    # merge namedtuples
    CityData = namedtuple("CityData", existing_cols + tuple(new_cols))
    for i, k in enumerate(citydata_narrow.keys()):
        citydata = CityData(*citydata_narrow[k], current_temperature[i], tomorrow_temperature[i], humidity[i],
                            current_weather_description[i])
        citydata_narrow[k] = citydata
    ret = citydata_narrow  # citydata_narrow is now wide, i.e. has the extra cols added
    log.info(f"<<< augment_city_data() returns: {pprint.pformat(ret)}")


def get_min_max_ints(citydata):
    log = logbook.Logger(__name__)
    log.info(f">>> get_min_max_ints(citydata={citydata})")
    min_max = {}
    for k, d in citydata.items():
        # print('%s is a %d year old %s' % p)
        for i, fld in enumerate(d._fields):
            # print(i,fld,d[i])
            t = min_max.get(fld)
            if not (t):
                min_max[fld] = [d[i], ] * 2
            else:
                if d[i] < t[0]:
                    t[0] = d[i]
                if d[i] > t[1]:
                    t[1] = d[i]
    log.info(f"<<< get_min_max_ints() returns: {pprint.pformat(min_max)}")
    return (min_max)


def do_all_dataload_steps():
    try:
        csv_filename = app.cfg.LOAD_DATA_CONFIG['csv_filename_to_load']
    except:
        raise InputDataCSVFileNotConfiguredError

    csv_filename = (pathlib.Path(app.cfg.root_fullpath) / csv_filename).as_posix()
    # csv_filename = 'test2.csv'
    app.cfg.all_cities_data = load_city_csv(csv_filename)
    #    print()

    augment_city_data(app.cfg.all_cities_data['loaded_data'])
    # pprint.pprint(res['loaded_data'])

    # The following step is not required but outputs the loaded validated data to a CSV file.
    csv_filename_loaded_data = app.cfg.LOAD_DATA_CONFIG.get('csv_filename_loaded_data')
    if csv_filename_loaded_data:
        write_city_csv(app.cfg.all_cities_data['loaded_data'], csv_filename_loaded_data)
    # print()
    # print(res)
    # pprint.pprint(res)

    # The following step is not required but outputs the min and max value for all data fields to application log
    # Used this information to help define the calc_city_score() function.
    min_max = get_min_max_ints(app.cfg.all_cities_data['loaded_data'])
    # print(min_max)
    # pprint.pprint(min_max)
