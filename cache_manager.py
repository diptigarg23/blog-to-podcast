"""
Caching system for blog content and podcasts.
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import CACHE_ENABLED, CACHE_EXPIRY_HOURS, CACHE_DIR
from utils import ensure_directory, save_json, load_json, generate_hash

class CacheManager:
    """Manages caching for blog content and generated files."""
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        self.enabled = CACHE_ENABLED
        self.expiry_hours = CACHE_EXPIRY_HOURS
        ensure_directory(self.cache_dir)
    
    def _get_cache_key(self, identifier: str) -> str:
        """Generate cache key from identifier."""
        return generate_hash(identifier)
    
    def _get_cache_path(self, cache_key: str, cache_type: str = 'content') -> str:
        """Get cache file path."""
        return os.path.join(self.cache_dir, f"{cache_type}_{cache_key}.json")
    
    def _is_expired(self, timestamp: str) -> bool:
        """Check if cache entry is expired."""
        if not timestamp:
            return True
        try:
            cache_time = datetime.fromisoformat(timestamp)
            expiry_time = cache_time + timedelta(hours=self.expiry_hours)
            return datetime.now() > expiry_time
        except:
            return True
    
    def get(self, identifier: str, cache_type: str = 'content') -> Optional[Dict[Any, Any]]:
        """Get cached content."""
        if not self.enabled:
            return None
        
        cache_key = self._get_cache_key(identifier)
        cache_path = self._get_cache_path(cache_key, cache_type)
        
        data = load_json(cache_path)
        if data and not self._is_expired(data.get('timestamp', '')):
            return data.get('content')
        elif data:
            # Expired, remove cache file
            try:
                os.remove(cache_path)
            except:
                pass
        
        return None
    
    def set(self, identifier: str, content: Dict[Any, Any], cache_type: str = 'content') -> bool:
        """Set cache content."""
        if not self.enabled:
            return False
        
        cache_key = self._get_cache_key(identifier)
        cache_path = self._get_cache_path(cache_key, cache_type)
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'identifier': identifier,
            'content': content
        }
        
        return save_json(cache_data, cache_path)
    
    def clear(self, cache_type: Optional[str] = None) -> int:
        """Clear cache entries. Returns number of files removed."""
        removed = 0
        try:
            if cache_type:
                pattern = f"{cache_type}_"
            else:
                pattern = ""
            
            for filename in os.listdir(self.cache_dir):
                if filename.startswith(pattern) and filename.endswith('.json'):
                    try:
                        os.remove(os.path.join(self.cache_dir, filename))
                        removed += 1
                    except:
                        pass
        except:
            pass
        
        return removed
    
    def clear_expired(self) -> int:
        """Clear expired cache entries."""
        removed = 0
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    cache_path = os.path.join(self.cache_dir, filename)
                    data = load_json(cache_path)
                    if data and self._is_expired(data.get('timestamp', '')):
                        try:
                            os.remove(cache_path)
                            removed += 1
                        except:
                            pass
        except:
            pass
        
        return removed
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = {
            'enabled': self.enabled,
            'total_files': 0,
            'expired_files': 0,
            'cache_size_mb': 0
        }
        
        try:
            total_size = 0
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    cache_path = os.path.join(self.cache_dir, filename)
                    stats['total_files'] += 1
                    total_size += os.path.getsize(cache_path)
                    
                    data = load_json(cache_path)
                    if data and self._is_expired(data.get('timestamp', '')):
                        stats['expired_files'] += 1
            
            stats['cache_size_mb'] = round(total_size / (1024 * 1024), 2)
        except:
            pass
        
        return stats

# Global cache manager instance
cache_manager = CacheManager()
