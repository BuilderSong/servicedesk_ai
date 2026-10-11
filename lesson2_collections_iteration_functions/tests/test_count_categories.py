from unittest import TestCase
from count_categories import count_categories

class TestCountCategories(TestCase):
    def test_count_categories(self):
        categories = ["Appliances", "appliances", "Blinds", "blinds", "Cabinets", "cabinets"]
        expected_output = {"appliances": 2, "blinds": 2, "cabinets": 2}
        self.assertEqual(count_categories(categories), expected_output)

    def test_count_categories_with_invalid_categories(self):
        categories = ["Appliances", "InvalidCategory", "Blinds", "AnotherInvalidCategory"]
        expected_output = {"appliances": 1, "blinds": 1}
        self.assertEqual(count_categories(categories), expected_output)

    def test_count_categories_with_empty_list(self):
        categories = []
        expected_output = {}
        self.assertEqual(count_categories(categories), expected_output) # type: ignore