from normalize_category import normalize_category as nc
import unittest

class TestNormalizeCategory(unittest.TestCase):
    def test_normalize_category(self):
        # Test with normal string
        self.assertEqual(nc("  Plumbing  "), "plumbing")
        
        # Test with already normalized string
        self.assertEqual(nc("Plumbing"), "plumbing")
        
        # Test with mixed case and whitespace
        self.assertEqual(nc("  PyThOn  "), "python")
        
        # Test with empty string (should raise ValueError)
        with self.assertRaises(ValueError):
            nc("")
        
        # Test with whitespace string (should raise ValueError)
        with self.assertRaises(ValueError):
            nc("   ")
        
        # Test with non-string input (should raise ValueError)
        with self.assertRaises(ValueError):
            nc(123) # type: ignore
        
        with self.assertRaises(ValueError):
            nc(None) # type: ignore
        
        # Test exceeding character limit (should raise ValueError)
        long_string = "a" * 41  # 41 characters
        with self.assertRaises(ValueError):
            nc(long_string)