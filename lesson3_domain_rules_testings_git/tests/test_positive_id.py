from positive_id import positive_id
from unittest import TestCase

class TestPositiveId(TestCase):
    def test_positive_id_with_positive_integer(self):
        self.assertEqual(positive_id(5), 5)
        
    def test_positive_id_with_zero(self):
        with self.assertRaises(ValueError):
            positive_id(0)

    def test_positive_id_with_negative_integer(self):
        with self.assertRaises(ValueError):
            positive_id(-3)

    def test_positive_id_with_non_integer(self):
        with self.assertRaises(ValueError):
            positive_id("string") # type: ignore

    def test_positive_id_with_boolean(self):
        with self.assertRaises(ValueError):
            positive_id(True)