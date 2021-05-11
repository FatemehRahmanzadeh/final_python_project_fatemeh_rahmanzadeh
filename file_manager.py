import json
from os import path
from datetime import datetime


def read_from_file(file_name, key=None):
    """
    this function is going to read from files and pass data to methods in other modules
    :param file_name: file name including format.json
    :param key: key of dictionary that is needed
    :return: a dictionary
    """
    if path.isfile(file_name):
        with open(f'{file_name}', 'r') as file:
            if key:
                execute = json.load(file)[key]
            else:
                execute = json.load(file)
            return execute
    else:
        return {}


def write_to_file(file_name, data, key1, key2=None):
    """
    this function takes a dictionary and writes it into an existing json file
    :param key: key of json file represents data as value
    :param file_name: file name including format.json
    :param data: a dictionary that is going to be write into file
    :return: a massage about writing successful
    """
    for val in data.values():
        if isinstance(val, datetime):
            data['work_datetime'] = f"{val.year}-{val.month}-{val.day} {val.time()}"

    if path.isfile(file_name):
        with open(file_name, 'r') as file:
            data_from_file = json.load(file)
            if key2:
                data_from_file[key1] = {key2: data}
            else:
                data_from_file[key1] = data

        with open(file_name, 'w') as file:
            json.dump(data_from_file, file, indent=4, ensure_ascii=False)
        return f'data has been written into {file_name} successfully'
    else:
        if key2:
            new_data = {key1:{key2: data}}
        else:
            new_data = {key1: data}
        with open(file_name, 'w') as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)

        return f'data has been written into {file_name} successfully'
