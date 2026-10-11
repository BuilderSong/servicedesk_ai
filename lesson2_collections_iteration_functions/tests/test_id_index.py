from id_index import id_index
from unittest import TestCase   

class TestIdIndex(TestCase):
    def test_id_index(self):
        records_list = [
            {1: "plumbing"},
            {2: "hvac"},
            {3: "electrical"}
        ]
        expected_output = {
            1: "plumbing",
            2: "hvac",
            3: "electrical"
        }
        self.assertEqual(id_index(records_list), expected_output)

    def test_id_index_with_duplicate_ids(self):
        records_list = [
            {1: "plumbing"},
            {2: "hvac"},
            {1: "electrical"}
        ]
        with self.assertRaises(ValueError):
            id_index(records_list)

    def test_id_index_with_empty_list(self):
        records_list = []
        expected_output = {}
        self.assertEqual(id_index(records_list), expected_output) # type: ignore
        
    def test_id_index_with_none(self):
        records_list = None
        with self.assertRaises(TypeError):
            id_index(records_list) # type: ignore