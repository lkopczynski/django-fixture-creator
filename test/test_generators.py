import unittest

from fixturecreator.fixturecreator.generators import RandomSequenceGenerator

class TestRandomSequenceGenerator(unittest.TestCase):

    def setUp(self):
        pass

    def test_min_max_length(self):
        self.rsg = RandomSequenceGenerator(min_length=5, max_length=8)
        value = self.rsg.value
        self.assertTrue(len(value) < 9)
        self.assertTrue(len(value) > 4)

    def test_exact_length(self):
        self.rsg = RandomSequenceGenerator(exact_length=8, characters='a')
        self.assertEqual(len(self.rsg.value), 8)

    def test_characters(self):
        self.rsg = RandomSequenceGenerator(exact_length=5, characters='a')
        self.assertEqual(self.rsg.value, 'aaaaa')
