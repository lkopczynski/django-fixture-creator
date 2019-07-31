import json
import random
import string
from datetime import datetime, timedelta

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


class RandomIntegerGenerator(BaseGenerator):
    def __init__(self, min_number=1, max_number=99, *args, **kwargs):
        self._min_number=int(min_number)
        self._max_number=int(max_number)
        super(RandomIntegerGenerator, self).__init__(*args, **kwargs)

    def _generate(self):
        return random.randint(self._min_number, self._max_number)


class RandomStringGenerator(RandomSequenceGenerator):
    def __init__(self, characters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ', *args, **kwargs):
        super(RandomStringGenerator, self).__init__(characters=characters, *args, **kwargs)


class VeryRandomDateGenerator(BaseGenerator):
    def __init__(self, *args, **kwargs):
        super(RandomDateGenerator, self).__init__(*args, **kwargs)

    def _generate(self):
        year = random.randint(1900, 2200)
        month = random.randint(1, 12)
        # nr of days based on month
        if month == 2:
            # check for leap-year
            if year % 4 != year % 100 or year % 400 == 0:
                day = random.randint(1, 29)
            else:
                day = random.randint(1, 28)
        elif month in [1,3,5,7,8,10,12]:
            day = random.randint(1,31)
        else:
            day = random.randint(1,30)

        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        rand_date = datetime( year, month, day, hour, minute, second)

class DateGenerator(BaseGenerator):
    def __init__(self, timedelta_in_days=0, *args, **kwargs):
        self.timedelta_in_days = timedelta_in_days
        super(DateGenerator, self).__init__(*args, **kwargs)

    def _generate(self):
        return str(datetime.now() + timedelta(hours=self.timedelta_in_days*24))

class RandomDateGenerator(DateGenerator):
    def _generate(self):
        if self.timedelta_in_days == 0:
            return super(RandomDateGenerator, self)._generate()
        elif self.timedelta_in_days > 0:
            minutes_delta = round(random.uniform(0, self.timedelta_in_days*24*60))
        else:
            minutes_delta = round(random.uniform(self.timedelta_in_days*24*60),0)

        return str(datetime.now() + timedelta(minutes=minutes_delta))
