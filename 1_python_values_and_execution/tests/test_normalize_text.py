from normalize_text import normalize_text as nt
import unittest

class TestNormalizeText(unittest.TestCase):
    def test_normalize_text(self):
        # Test with normal string
        self.assertEqual(nt("  Plumbing  "), "plumbing")
        
        # Test with already normalized string
        self.assertEqual(nt("Plumbing"), "plumbing")
        
        # Test with already normalized string
        self.assertEqual(nt("Plum  bing"), "plum  bing")
        
        
        # Test with empty string (should raise ValueError)
        with self.assertRaises(ValueError):
            nt("")
        
        # Test with whitespace string (should raise ValueError)
        with self.assertRaises(ValueError):
            nt("  ")
        
        # Test with non-string input (should raise ValueError)
        with self.assertRaises(ValueError):
            nt(12) # type: ignore
        
        with self.assertRaises(ValueError):
            nt(None) # type: ignore

