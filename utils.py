"""
Common utilities and helper functions.
"""

import os
import re
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
import json

def ensure_directory(path: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    os.makedirs(path, exist_ok=True)

def clean_filename(filename: str) -> str:
    """Clean a filename to remove invalid characters."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def generate_hash(text: str) -> str:
    """Generate a hash from text for caching purposes."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable format."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}secs"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def is_forrester_url(url: str) -> bool:
    """Check if URL is from Forrester domain."""
    forrester_domains = ['forrester.com', 'blogs.forrester.com', 'www.forrester.com']
    return any(domain in url.lower() for domain in forrester_domains)

def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to maximum length with suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL."""
    match = re.search(r'https?://([^/]+)', url)
    return match.group(1) if match else None

def save_json(data: Dict[Any, Any], filepath: str) -> bool:
    """Save data to JSON file."""
    try:
        ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def load_json(filepath: str) -> Optional[Dict[Any, Any]]:
    """Load data from JSON file."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
    return None

def get_timestamp() -> str:
    """Get current timestamp as string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sanitize_text(text: str) -> str:
    """Sanitize text by removing excessive whitespace and special characters."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    return text.strip()

def chunk_text_by_sentences(text: str, max_chunk_size: int) -> list:
    """Split text into chunks by sentences, respecting max chunk size."""
    sentences = re.split(r'([.!?]+[ \n])', text)
    chunks = []
    current_chunk = ""
    
    for i in range(0, len(sentences), 2):
        sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '')
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
