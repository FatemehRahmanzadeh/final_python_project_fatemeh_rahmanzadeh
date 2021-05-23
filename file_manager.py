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


def write_to_file(file_name, data, key1=None, key2=None):
    """
    this function takes a dictionary and writes it into an existing json file
    :param key1: key of json file represents data as value if there was no inner key
    :param key2: inner key of json file represents data as value if data were dict of inner data.
    for example, in users work file key1 is username, key2 is work name
    :param file_name: file name including format.json
    :param data: a dictionary that is going to be write into file
    :return: a massage about writing successful
    """
    for key, val in data.items():
        if isinstance(val, datetime):
            data[key] = f"{val.date()} {val.time()}"
    try:
        assert path.isfile(file_name)
        with open(file_name, 'r') as file:
            data_from_file = json.load(file)

            if key1 in data_from_file.keys() and key2:
                data_from_file[key1].update({key2: data})

            elif (key1 in data_from_file.keys()) and (not key2):
                data_from_file[key1] = data

            elif key1 not in data_from_file.keys() and key2:
                data_from_file[key1] = {key2: data}

            elif key1 not in data_from_file.keys() and (not key2):
                data_from_file.update({key1: data})

        with open(file_name, 'w') as file:
            json.dump(data_from_file, file, indent=4, ensure_ascii=False)
        return f'data has been written into {file_name} successfully'
    except AssertionError:
        print('file does not exist. creating new file.')
        new_data = {}
        if key1 and key2:
            new_data = {key1:{key2: data}}
        elif key1 and not key2:
            new_data = {key1: data}
        elif not key1 and key2:
            print('missing username as key..')

        with open(file_name, 'w') as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)

        return f'data has been written into {file_name} successfully'


def user_lock_r(file_lock):
    """
    this function is for saving username of locked account and reading from it.
    :param file_lock: json file name
    :return:a dictionary of usernames and time they locked
    """

    if not path.isfile(file_lock):
        return {}
    else:
        with open(file_lock, 'r') as file:
            return json.load(file)


def user_lock_w(file_lock, username, time):
    """
    this function is for saving username of locked account and reading from it.
    :param file_lock: json file name
    :param username: locked username
    :param time: datetime of lock
    :return:a massage
    """

    if not path.isfile(file_lock):
        with open(file_lock, 'w') as file:
            json.dump({username: time}, file, indent=4, ensure_ascii=False)
    else:
        with open(file_lock, 'r') as file:
            data_file = json.load(file)
        data_file[username] = time

        with open(file_lock, 'w') as file:
            json.dump(data_file, file, indent=4, ensure_ascii=False)
    return f"lock information saved"