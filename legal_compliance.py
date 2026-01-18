"""
Legal compliance and attribution handling.
"""

from typing import Dict, Optional
from datetime import datetime
from config import (
    ENABLE_EXCERPT_LIMITS,
    MAX_EXCERPT_LENGTH,
    REQUIRE_TERMS_ACKNOWLEDGMENT,
    SHOW_LEGAL_DISCLAIMER
)
from utils import truncate_text

LEGAL_DISCLAIMER = """
**Legal Disclaimer**

This application is for educational and portfolio demonstration purposes. Content from Forrester blog posts is used with proper attribution and in accordance with fair use principles for educational purposes.

- All content is attributed to its original source
- This tool does not claim ownership of Forrester content
- Users are responsible for ensuring their use complies with Forrester's Terms of Use
- For commercial use, please obtain proper licensing from Forrester

For more information, please refer to:
- [Forrester Terms of Use](https://www.forrester.com/policies/terms-of-use/)
- [Forrester Citation Policy](https://www.forrester.com/policies/citations-policy/)
"""

def generate_attribution(metadata: Dict) -> str:
    """
    Generate attribution text for blog content.
    
    Args:
        metadata: Dictionary containing title, author, date, url
        
    Returns:
        Attribution string
    """
    attribution_parts = []
    
    if metadata.get('title'):
        attribution_parts.append(f"**Title:** {metadata['title']}")
    
    if metadata.get('author'):
        attribution_parts.append(f"**Author:** {metadata['author']}")
    
    if metadata.get('date'):
        attribution_parts.append(f"**Date:** {metadata['date']}")
    
    if metadata.get('url'):
        attribution_parts.append(f"**Source:** [{metadata['url']}]({metadata['url']})")
    
    attribution_parts.append("\n*Content used with attribution for educational/portfolio purposes.*")
    
    return "\n\n".join(attribution_parts)

def apply_excerpt_limits(content: str) -> str:
    """
    Apply excerpt limits to content if enabled.
    
    Args:
        content: Original content
        
    Returns:
        Limited content if limits enabled, otherwise original content
    """
    if not ENABLE_EXCERPT_LIMITS:
        return content
    
    if len(content) > MAX_EXCERPT_LENGTH:
        return truncate_text(content, MAX_EXCERPT_LENGTH, 
                           suffix=f"\n\n[... Content truncated. Full article available at source URL ...]")
    
    return content

def get_legal_disclaimer() -> str:
    """Get legal disclaimer text."""
    return LEGAL_DISCLAIMER if SHOW_LEGAL_DISCLAIMER else ""

def check_terms_acknowledgment_required() -> bool:
    """Check if terms acknowledgment is required."""
    return REQUIRE_TERMS_ACKNOWLEDGMENT

def create_attribution_metadata(url: str, title: Optional[str] = None, 
                               author: Optional[str] = None, 
                               date: Optional[str] = None) -> Dict:
    """
    Create attribution metadata dictionary.
    
    Args:
        url: Source URL
        title: Article title
        author: Author name
        date: Publication date
        
    Returns:
        Metadata dictionary
    """
    return {
        'url': url,
        'title': title or 'Untitled',
        'author': author or 'Unknown',
        'date': date or datetime.now().strftime('%Y-%m-%d'),
        'accessed_at': datetime.now().isoformat()
    }

def validate_content_usage(content: str, metadata: Dict) -> Dict[str, any]:
    """
    Validate content usage and return compliance status.
    
    Args:
        content: Content to validate
        metadata: Content metadata
        
    Returns:
        Dictionary with compliance status and warnings
    """
    result = {
        'compliant': True,
        'warnings': [],
        'recommendations': []
    }
    
    # Check content length
    if len(content) > 10000:
        result['warnings'].append(
            "Large content detected. Consider using excerpts for better compliance."
        )
    
    # Check if attribution is present
    if not metadata.get('url'):
        result['warnings'].append("Source URL missing in metadata.")
        result['compliant'] = False
    
    # Recommendations
    if not ENABLE_EXCERPT_LIMITS:
        result['recommendations'].append(
            "Consider enabling excerpt limits for better compliance."
        )
    
    return result
