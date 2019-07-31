import json
import random
import string

class BaseGenerator:
    _value = None

    def _generate(self):
        pass

    @property
    def value(self):
        self._value = self._generate()
        return self._value


class RandomSequenceGenerator(BaseGenerator):
    _characters = ''

    def __init__(self, min_length=1, max_length=10, length=None, characters='abAB'):
        if length is not None:
            self._min_length = self._max_length = int(length)
        else:
            self._min_length = min_length
            self._max_length = max_length
        self._characters = characters

    def _generate(self):
        return ''.join(random.choice(self._characters) for i in range(random.randint(self._min_length, self._max_length)))


class RandomStringGenerator(RandomSequenceGenerator):
    def __init__(self, characters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ', *args, **kwargs):
        super(RandomStringGenerator, self).__init__(*args, **kwargs)
