import json


class FixtureCreator:

    pattern = None

    def __init__(self):
        pass

    def loadPattern(self, json_string):
        self.pattern = json.loads(json)


    def go_over_pattern(self):
        if pattern is None:
            raise ValueError('No pattern defined!')
