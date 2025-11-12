import unittest
from src.nbt_parser import NbtParser

class TestNbtParser(unittest.TestCase):

    def setUp(self):
        self.parser = NbtParser()

    def test_parse_snbt(self):
        snbt_string = '{"key": "value", "number": 123, "list": [1, 2, 3]}'
        expected_output = {
            'key': 'value',
            'number': 123,
            'list': [1, 2, 3]
        }
        result = self.parser.parse_snbt(snbt_string)
        self.assertEqual(result, expected_output)

    def test_to_json(self):
        nbt_data = {
            'key': 'value',
            'number': 123,
            'list': [1, 2, 3]
        }
        expected_json = '{"key": "value", "number": 123, "list": [1, 2, 3]}'
        result = self.parser.to_json(nbt_data)
        self.assertEqual(result, expected_json)

if __name__ == '__main__':
    unittest.main()