import json

from fixturecreator import FixtureCreator

f = FixtureCreator()
with open('fixturepattern.json') as pattern_file:
    json_data = json.dumps(json.load(pattern_file))


print(f.create_from_json(json_data))
