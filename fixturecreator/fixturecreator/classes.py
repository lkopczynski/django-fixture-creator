import json
import random


class FixtureCreator:

    generators = [
        ('string', 'RandomStringGenerator')
    ]

    _pattern = None
    _elements = []

    def __init__(self):
        pass

    def load_pattern(self, json_string):
        self._pattern = json.loads(json_string)

    def go_over_pattern(self):
        if self._pattern is None:
            raise ValueError('No pattern defined!')

        for element in self._pattern:
            self._create_element(element)

    def _create_element(self, data):
        element = {
            "model": data['model'],
            "pk": random.randint(1, 100000)
        }

        for field in data['fields']:
            print(field['type'])
