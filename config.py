"""
Configuration management for Blog to Podcast Platform.
All settings and default parameters.
"""

# Application Settings
APP_NAME = "Blog to Podcast Converter"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Transform Forrester blog posts into engaging podcasts"

# TTS Engine Selection
# Using Google Text-to-Speech (gTTS) as the only TTS engine

# TTS Settings
DEFAULT_LANGUAGE = 'en'
DEFAULT_VOICE_SPEED = 1.0
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'zh': 'Chinese',
    'ja': 'Japanese'
}

# Audio Settings
AUDIO_FORMAT = 'mp3'
AUDIO_QUALITY = 'high'  # 'low', 'medium', 'high'
MAX_AUDIO_CHUNK_SIZE = 4500  # Characters per chunk for TTS

# Blog Scraping Settings
REQUEST_TIMEOUT = 10  # seconds
REQUEST_DELAY = 1  # seconds between requests
MAX_CONTENT_LENGTH = 50000  # Maximum characters to process
CACHE_ENABLED = True
CACHE_EXPIRY_HOURS = 24

# Legal Compliance Settings
ENABLE_EXCERPT_LIMITS = False  # Set to True to limit content
MAX_EXCERPT_LENGTH = 1000  # Characters if limits enabled
REQUIRE_TERMS_ACKNOWLEDGMENT = True
SHOW_LEGAL_DISCLAIMER = True

# File Storage
TEMP_DIR = './temp'
OUTPUT_DIR = './output'
CACHE_DIR = './cache'

# UI Settings
THEME_PRIMARY_COLOR = "#1f77b4"
THEME_BACKGROUND_COLOR = "#ffffff"
THEME_SECONDARY_COLOR = "#666666"

# Feature Flags
ENABLE_SETTINGS_PAGE = True
ENABLE_BATCH_PROCESSING = False
ENABLE_USER_AUTH = False
