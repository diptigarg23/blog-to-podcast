"""
Tests for blog_fetcher module.
"""

import unittest
from blog_fetcher import fetch_from_text, validate_url, is_forrester_url

class TestBlogFetcher(unittest.TestCase):
    """Test cases for blog fetcher."""
    
    def test_fetch_from_text(self):
        """Test fetching from pasted text."""
        text = "This is a sample blog post content. It has multiple sentences."
        result = fetch_from_text(text)
        
        self.assertIsNotNone(result)
        self.assertIn('content', result)
        self.assertIn('metadata', result)
        self.assertEqual(result['content'], text.strip())
    
    def test_validate_url(self):
        """Test URL validation."""
        self.assertTrue(validate_url("https://www.forrester.com/blog/test"))
        self.assertTrue(validate_url("http://example.com"))
        self.assertFalse(validate_url("not-a-url"))
        self.assertFalse(validate_url(""))
    
    def test_is_forrester_url(self):
        """Test Forrester URL detection."""
        self.assertTrue(is_forrester_url("https://www.forrester.com/blog/test"))
        self.assertTrue(is_forrester_url("https://blogs.forrester.com/article"))
        self.assertFalse(is_forrester_url("https://example.com/blog"))

if __name__ == '__main__':
    unittest.main()
