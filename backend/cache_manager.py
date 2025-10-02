"""
Cache management module for SUME Smart Summarizer
Handles in-memory caching for performance optimization
"""
import hashlib
from functools import wraps

# Simple in-memory cache for performance
cache = {}

def cache_result(func):
    """Cache decorator for expensive operations"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key from function name and arguments
        cache_key = f"{func.__name__}_{hashlib.md5(str(args).encode()).hexdigest()}"
        if cache_key in cache:
            return cache[cache_key]
        result = func(*args, **kwargs)
        cache[cache_key] = result
        return result
    return wrapper

def clear_cache():
    """Clear the in-memory cache"""
    global cache
    cache.clear()
    return "Cache cleared successfully!"

def get_cache_stats():
    """Get cache statistics"""
    return f"Cache size: {len(cache)} items"
