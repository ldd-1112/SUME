"""
Cache management module for SUME Smart Summarizer
Handles in-memory caching for performance optimization with TTL and size limits
"""
import hashlib
import time
import json
from functools import wraps
from typing import Any, Dict, Optional

# Enhanced cache with TTL and size management
cache: Dict[str, Dict[str, Any]] = {}
CACHE_MAX_SIZE = 1000  # Maximum number of cached items
CACHE_TTL = 3600  # Time to live in seconds (1 hour)

class CacheItem:
    """Cache item with timestamp and data"""
    def __init__(self, data: Any, ttl: int = CACHE_TTL):
        self.data = data
        self.timestamp = time.time()
        self.ttl = ttl
    
    def is_expired(self) -> bool:
        """Check if cache item has expired"""
        return time.time() - self.timestamp > self.ttl
    
    def get_data(self) -> Any:
        """Get data if not expired, otherwise return None"""
        return self.data if not self.is_expired() else None

def _create_cache_key(func_name: str, args: tuple, kwargs: dict) -> str:
    """Create a more robust cache key"""
    # Sort kwargs for consistent key generation
    sorted_kwargs = sorted(kwargs.items()) if kwargs else []
    key_data = f"{func_name}_{args}_{sorted_kwargs}"
    return hashlib.sha256(key_data.encode()).hexdigest()[:16]

def _cleanup_expired():
    """Remove expired items from cache"""
    global cache
    expired_keys = [key for key, item in cache.items() if item.is_expired()]
    for key in expired_keys:
        del cache[key]

def _enforce_size_limit():
    """Remove oldest items if cache exceeds size limit"""
    global cache
    if len(cache) > CACHE_MAX_SIZE:
        # Sort by timestamp and remove oldest items
        sorted_items = sorted(cache.items(), key=lambda x: x[1].timestamp)
        items_to_remove = len(cache) - CACHE_MAX_SIZE
        for key, _ in sorted_items[:items_to_remove]:
            del cache[key]

def cache_result(ttl: int = CACHE_TTL):
    """Enhanced cache decorator with TTL and size management"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Clean up expired items first
            _cleanup_expired()
            
            # Create cache key
            cache_key = _create_cache_key(func.__name__, args, kwargs)
            
            # Check if item exists and is not expired
            if cache_key in cache:
                cached_item = cache[cache_key]
                if not cached_item.is_expired():
                    return cached_item.get_data()
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            
            # Store in cache with TTL
            cache[cache_key] = CacheItem(result, ttl)
            
            # Enforce size limit
            _enforce_size_limit()
            
            return result
        return wrapper
    return decorator

def clear_cache():
    """Clear the in-memory cache"""
    global cache
    cache.clear()
    return "Cache cleared successfully!"

def get_cache_stats():
    """Get detailed cache statistics"""
    _cleanup_expired()
    total_items = len(cache)
    expired_items = sum(1 for item in cache.values() if item.is_expired())
    active_items = total_items - expired_items
    
    # Calculate memory usage estimate
    memory_estimate = sum(len(str(item.data)) for item in cache.values())
    
    return f"Cache: {active_items} active items, {expired_items} expired, ~{memory_estimate} chars"

def get_cache_info():
    """Get detailed cache information for debugging"""
    _cleanup_expired()
    info = {
        "total_items": len(cache),
        "max_size": CACHE_MAX_SIZE,
        "ttl": CACHE_TTL,
        "memory_usage": sum(len(str(item.data)) for item in cache.values()),
        "oldest_item": min((item.timestamp for item in cache.values()), default=0),
        "newest_item": max((item.timestamp for item in cache.values()), default=0)
    }
    return json.dumps(info, indent=2)
