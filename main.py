import sys
import os

import yaml
import schemas
from jsonschema import validate

from engine import Engine

if sys.platform == 'win32':
    os.system('chcp 65001')


def main(input_file, keys):

    # Load the main input file
    with open(input_file, 'r') as stream:
        instructions = yaml.load(stream)

    # Validate the input file
    validate(instructions, schemas.load(instructions['version']))

    with open(keys, 'r') as stream:
        keys = yaml.load(stream)

    # Load the necessary components into the engine
    engine = Engine(instructions, keys)

    # Run the engine
    engine.run()


if __name__ == '__main__':
    input_file = 'input.yaml'
    keys = 'my_keys.yaml'
    main(input_file, keys)
