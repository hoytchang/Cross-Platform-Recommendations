from os.path import dirname, join

import json


def load(version):
    directory = dirname(__file__)
    with open(join(directory, version + '.json')) as f:
        data = json.load(f)
    return data
