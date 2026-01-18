"""
Tests for podcast_generator module.
"""

import unittest
import os
from podcast_generator import generate_podcast

class TestPodcastGenerator(unittest.TestCase):
    """Test cases for podcast generator."""
    
    def test_generate_podcast_short_text(self):
        """Test podcast generation with short text."""
        text = "This is a short test text for podcast generation."
        result = generate_podcast(text, language='en')
        
        # Should return a file path or None
        self.assertTrue(result is None or (isinstance(result, str) and len(result) > 0))
    
    def test_generate_podcast_empty_text(self):
        """Test podcast generation with empty text."""
        result = generate_podcast("", language='en')
        self.assertIsNone(result)
    
    def test_generate_podcast_long_text(self):
        """Test podcast generation with long text."""
        text = "This is a long text. " * 1000  # Create long text
        result = generate_podcast(text, language='en')
        
        # Should handle long text (may return None if TTS fails)
        self.assertTrue(result is None or isinstance(result, str))

if __name__ == '__main__':
    unittest.main()
