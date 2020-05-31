""" Program that gets COVID19 information related to Czechia """
import configparser
import os
import re
import pandas as pd
from flask import Flask, request, jsonify

config = configparser.ConfigParser(os.environ)
config.read('configuration.ini')

EXTENSION = ".csv"
PATH = config['parameters']['path']


def get_all_files(search_path, extension):
    """ Returns a list with all files with specific extension under the
    specified path """
    list_of_files = []
    for path, subdir, files in os.walk(search_path):
        for file in files:
            if file.endswith(extension):
                list_of_files.append(os.path.join(path, file))
    return list_of_files


def files_for_country(search_path, extension, country_name):
    """ Returns a list with all files that contain a specific country name """
    list_of_files = []
    for filename in get_all_files(search_path, extension):
        with open(filename, 'r') as file:
            for line in file:
                if country_name in line:
                    list_of_files.append(filename)
    return list_of_files


def get_country_info(search_path, extension, country):
    """ Returns a list of dictionaries with information for a specific country
    """
    list_of_json_strings = []
    columns_to_check = ['FIPS', 'Admin2', 'Province_State',
                        'Province/State', 'Province/States']
    columns_to_drop = []
    for filename in files_for_country(search_path, extension, country):
        data = pd.read_csv(filename, index_col=False, nrows=1)
        headers = list(data)
        # Find columns to be dropped because they contain NaN values
        columns_to_drop = [i for i in headers if i in columns_to_check]
        # Find the column name that contains the keyword Country
        reg = re.compile("Country*")
        column_name = list(filter(reg.match, headers))
        data = pd.read_csv(filename, index_col=False)
        entry = (data[data[column_name[0]] ==
                      country]).drop(columns_to_drop,
                                     axis=1).to_dict('records')
        list_of_json_strings.append(entry)
    return list_of_json_strings

app = Flask(__name__)


@app.route('/countries', methods=['GET'])
def get_country():
    """ Calls the function that shows the country's information
    """
    country = request.args.get('country')
    return jsonify(get_country_info(PATH, EXTENSION, country))


@app.route('/health', methods=['GET'])
def health():
    """ Checks the health of the API
    """
    return {'Status': 'Healthy'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
