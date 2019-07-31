import json
import random
import importlib


class FixtureCreator:

    _generators = [
        ('string', 'RandomStringGenerator'),
        ('stringrandom', 'RandomStringGenerator'),
        ('date', 'DateGenerator'),
        ('daterandom', 'RandomDateGenerator'),
        ('integer', 'RandomIntegerGenerator')
    ]

    _pattern = None
    _elements = []
    _pks_used = {}

    def __init__(self):
        pass

    def load_pattern(self, json_string):
        self._pattern = json.loads(json_string)

    def go_over_pattern(self):
        if self._pattern is None:
            raise ValueError('No pattern defined!')

        for element in self._pattern:
            if 'count' in element:
                for _ in range(element['count']):
                    self._create_element(element)
            else:
                self._create_element(element)

    def create_from_json(self, json_string):
        self.load_pattern(json_string)
        self.go_over_pattern()
        return json.dumps(self._elements)

    def register_generator(self, designation, class_path):
        for generator in self._generators:
            if generator[0] == designation:
                raise KeyError(f'Designation {designation} already points to {generator[1]}')
        self._generators.append((designation, class_path))

    def _get_generator(self, designation, settings):
        for generator in self._generators:
            if generator[0] == designation:
                module = importlib.import_module('fixturecreator.generators')
                class_ = getattr(module, generator[1])
                return class_(**settings)
        raise KeyError(f'No generator for designation {designation} found!')

    def _add_used_pk(self, model, pk):
        model = str(model)
        pk = int(pk)
        if not model in self._pks_used:
            self._pks_used[model] = []
        if pk in self._pks_used[model]:
            raise ValueError('This PK is already in use!')
        self._pks_used[model].append(pk)

    def _get_unused_pk(self, model):
        model = str(model)
        if not model in self._pks_used:
            self._pks_used[model] = []
        while True:
            rand_max = (len(self._pks_used[model])+1)*2
            curr_pk = random.randint(1,rand_max)
            if curr_pk not in self._pks_used[model]:
                break
        self._pks_used[model].append(curr_pk)
        return curr_pk

    def _create_field(self, field_data):
        field_type = str(field_data['type'])
        field_name = str(field_data['name'])

        if 'content' in field_data:
            return {field_name: field_data['content']}
        if field_type == 'foreignkey' and 'object' in field_data:
            print('yo')
            new_element_pk = self._create_element(field_data['object'])
            return { field_name: new_element_pk }
        if 'generator' in field_data:
            gen = self._get_generator(f'{field_type}{field_data["generator"]}', field_data['settings'])
            return { field_name: gen.value }

        return {}

    def _create_element(self, data):
        model = str(data['model'])
        # create element dict
        element = {
            'model': model,
            'fields': []
        }

        # add pk from data if provided, else generate a new one
        if 'pk' in data:
            pk = int(data['pk'])
            self._add_used_pk(model, pk)
            element['pk'] = pk
        else:
            element['pk'] = self._get_unused_pk(data['model'])

        # generate all the fields
        for field in data['fields']:
            element['fields'].append(self._create_field(field))

        self._elements.append(element)
        return element['pk']
