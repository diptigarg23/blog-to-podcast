"""
Enhanced blog content extraction from Forrester blog posts.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Dict, Optional
from urllib.parse import urlparse, urljoin
from config import REQUEST_TIMEOUT, REQUEST_DELAY, MAX_CONTENT_LENGTH
from utils import validate_url, is_forrester_url, sanitize_text, extract_domain
from cache_manager import cache_manager
from legal_compliance import create_attribution_metadata

def check_robots_txt(url: str) -> bool:
    """
    Check robots.txt to see if scraping is allowed.
    Returns True if allowed, False if disallowed.
    """
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            # Simple check - in production, use robotparser
            robots_content = response.text.lower()
            if 'disallow: /' in robots_content or 'disallow: /blog' in robots_content:
                return False
    except:
        pass
    return True

def extract_metadata(soup: BeautifulSoup, url: str) -> Dict:
    """Extract metadata from blog post."""
    metadata = {
        'url': url,
        'title': None,
        'author': None,
        'date': None,
        'tags': [],
        'description': None
    }
    
    # Extract title
    title_selectors = [
        'h1',
        '.post-title',
        '.article-title',
        '.blog-title',
        '[property="og:title"]',
        'title'
    ]
    for selector in title_selectors:
        element = soup.select_one(selector)
        if element:
            metadata['title'] = element.get_text(strip=True) or element.get('content', '')
            if metadata['title']:
                break
    
    # Extract author
    author_selectors = [
        '.author',
        '.post-author',
        '.article-author',
        '[rel="author"]',
        '[property="article:author"]'
    ]
    for selector in author_selectors:
        element = soup.select_one(selector)
        if element:
            metadata['author'] = element.get_text(strip=True) or element.get('content', '')
            if metadata['author']:
                break
    
    # Extract date
    date_selectors = [
        '.date',
        '.post-date',
        '.article-date',
        '.published',
        'time',
        '[property="article:published_time"]'
    ]
    for selector in date_selectors:
        element = soup.select_one(selector)
        if element:
            date_text = element.get_text(strip=True) or element.get('content', '') or element.get('datetime', '')
            if date_text:
                metadata['date'] = date_text
                break
    
    # Extract description
    desc_element = soup.select_one('meta[name="description"]') or soup.select_one('[property="og:description"]')
    if desc_element:
        metadata['description'] = desc_element.get('content', '')
    
    # Extract tags
    tag_elements = soup.select('.tags a, .tag, [rel="tag"]')
    metadata['tags'] = [tag.get_text(strip=True) for tag in tag_elements if tag.get_text(strip=True)]
    
    return metadata

def extract_content(soup: BeautifulSoup) -> str:
    """Extract main content from blog post."""
    # Remove unwanted elements
    for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 
                        'advertisement', 'ad', '.ad', '.sidebar', '.comments']):
        element.decompose()
    
    # Try to find main content area
    content_selectors = [
        'article',
        '.post-content',
        '.blog-content',
        '.article-content',
        '.entry-content',
        'main',
        '.content',
        '[role="main"]',
        '.post-body'
    ]
    
    content = None
    for selector in content_selectors:
        content = soup.select_one(selector)
        if content:
            break
    
    # Fallback to body if no specific content area found
    if not content:
        content = soup.find('body')
    
    if not content:
        return ""
    
    # Extract text with structure preservation
    paragraphs = []
    for element in content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
        text = element.get_text(separator=' ', strip=True)
        if text and len(text) > 10:  # Filter very short elements
            # Preserve heading structure
            if element.name.startswith('h'):
                paragraphs.append(f"\n\n{text}\n")
            else:
                paragraphs.append(text)
    
    # Combine paragraphs
    full_text = '\n\n'.join(paragraphs)
    
    # Clean up
    full_text = re.sub(r'\n{3,}', '\n\n', full_text)
    full_text = sanitize_text(full_text)
    
    return full_text

def fetch_blog_content(url: str, use_cache: bool = True) -> Optional[Dict]:
    """
    Fetch and extract content from a Forrester blog post URL.
    
    Args:
        url: The URL of the blog post
        use_cache: Whether to use cached content if available
        
    Returns:
        Dictionary with 'content', 'metadata', and 'raw_html' keys, or None if failed
    """
    if not validate_url(url):
        return None
    
    # Check cache
    if use_cache:
        cached = cache_manager.get(url, 'blog_content')
        if cached:
            return cached
    
    # Respect rate limiting
    time.sleep(REQUEST_DELAY)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract metadata
        metadata = extract_metadata(soup, url)
        
        # Extract content
        content = extract_content(soup)
        
        # Limit content length
        if len(content) > MAX_CONTENT_LENGTH:
            content = content[:MAX_CONTENT_LENGTH] + "\n\n[... Content truncated ...]"
        
        if not content:
            return None
        
        # Create result
        result = {
            'content': content,
            'metadata': metadata,
            'raw_html': response.text[:10000] if len(response.text) < 10000 else response.text[:10000] + '...',  # Store first 10k chars
            'fetched_at': time.time()
        }
        
        # Cache result
        if use_cache:
            cache_manager.set(url, result, 'blog_content')
        
        return result
        
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error parsing content: {e}")
        return None

def fetch_from_text(text: str, url: Optional[str] = None) -> Dict:
    """
    Create blog data structure from pasted text.
    
    Args:
        text: Pasted text content
        url: Optional source URL
        
    Returns:
        Dictionary with content and metadata
    """
    metadata = create_attribution_metadata(
        url=url or 'Pasted Content',
        title='User Provided Content',
        author='User',
        date=None
    )
    
    # Limit content length
    if len(text) > MAX_CONTENT_LENGTH:
        text = text[:MAX_CONTENT_LENGTH] + "\n\n[... Content truncated ...]"
    
    return {
        'content': sanitize_text(text),
        'metadata': metadata,
        'raw_html': None,
        'fetched_at': time.time()
    }
