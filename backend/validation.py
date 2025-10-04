"""
Input validation module for SUME Smart Summarizer
Handles validation of inputs to prevent unnecessary processing
"""
import os
import re
import urllib.parse
from typing import Tuple, Optional, List

# File size limits (in bytes)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_TEXT_LENGTH = 1000000  # 1M characters
MAX_URL_LENGTH = 2048

# Supported file extensions
SUPPORTED_TEXT_EXTENSIONS = {'.txt', '.md', '.docx', '.pdf'}
SUPPORTED_MEDIA_EXTENSIONS = {'.mp3', '.mp4', '.wav', '.m4a', '.webm', '.avi', '.mov'}

def validate_text_input(text: str) -> Tuple[bool, str]:
    """Validate text input for summarization"""
    if not text or not isinstance(text, str):
        return False, "⚠️ Text input is required and must be a string."
    
    if len(text.strip()) < 10:
        return False, "⚠️ Text must be at least 10 characters long."
    
    if len(text) > MAX_TEXT_LENGTH:
        return False, f"⚠️ Text is too long. Maximum {MAX_TEXT_LENGTH:,} characters allowed."
    
    # Check for meaningful content (not just whitespace or repeated characters)
    cleaned_text = re.sub(r'\s+', ' ', text.strip())
    if len(cleaned_text) < 10:
        return False, "⚠️ Text must contain meaningful content."
    
    # Check for excessive repetition
    words = cleaned_text.split()
    if len(words) > 10:
        unique_words = len(set(word.lower() for word in words))
        if unique_words / len(words) < 0.3:  # Less than 30% unique words
            return False, "⚠️ Text appears to have excessive repetition."
    
    return True, "Valid text input."

def validate_file_input(file_path: str) -> Tuple[bool, str, Optional[str]]:
    """Validate file input for processing"""
    if not file_path or not isinstance(file_path, str):
        return False, "⚠️ File path is required.", None
    
    if not os.path.exists(file_path):
        return False, "⚠️ File does not exist.", None
    
    # Check file size
    try:
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            return False, f"⚠️ File is too large. Maximum {MAX_FILE_SIZE // (1024*1024)}MB allowed.", None
        
        if file_size == 0:
            return False, "⚠️ File is empty.", None
    except OSError:
        return False, "⚠️ Cannot access file.", None
    
    # Check file extension
    _, ext = os.path.splitext(file_path.lower())
    if ext not in SUPPORTED_TEXT_EXTENSIONS:
        return False, f"⚠️ Unsupported file type: {ext}. Supported: {', '.join(SUPPORTED_TEXT_EXTENSIONS)}", None
    
    return True, "Valid file input.", ext

def validate_media_file(file_path: str) -> Tuple[bool, str, Optional[str]]:
    """Validate media file input for processing"""
    if not file_path or not isinstance(file_path, str):
        return False, "⚠️ Media file path is required.", None
    
    if not os.path.exists(file_path):
        return False, "⚠️ Media file does not exist.", None
    
    # Check file size
    try:
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE * 2:  # Media files can be larger
            return False, f"⚠️ Media file is too large. Maximum {MAX_FILE_SIZE * 2 // (1024*1024)}MB allowed.", None
        
        if file_size == 0:
            return False, "⚠️ Media file is empty.", None
    except OSError:
        return False, "⚠️ Cannot access media file.", None
    
    # Check file extension
    _, ext = os.path.splitext(file_path.lower())
    if ext not in SUPPORTED_MEDIA_EXTENSIONS:
        return False, f"⚠️ Unsupported media type: {ext}. Supported: {', '.join(SUPPORTED_MEDIA_EXTENSIONS)}", None
    
    return True, "Valid media file input.", ext

def validate_url(url: str) -> Tuple[bool, str]:
    """Validate URL input"""
    if not url or not isinstance(url, str):
        return False, "⚠️ URL is required and must be a string."
    
    if len(url) > MAX_URL_LENGTH:
        return False, f"⚠️ URL is too long. Maximum {MAX_URL_LENGTH} characters allowed."
    
    # Parse URL
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme:
            url = "http://" + url
            parsed = urllib.parse.urlparse(url)
        
        if not parsed.netloc:
            return False, "⚠️ Invalid URL format."
        
        # Check for suspicious patterns
        if any(pattern in url.lower() for pattern in ['javascript:', 'data:', 'file:']):
            return False, "⚠️ URL contains potentially unsafe content."
        
        return True, "Valid URL input."
    except Exception:
        return False, "⚠️ Invalid URL format."

def validate_language(language: str) -> Tuple[bool, str]:
    """Validate language input for translation"""
    if not language or not isinstance(language, str):
        return False, "⚠️ Language is required and must be a string."
    
    # Basic validation - check for reasonable length and characters
    if len(language.strip()) < 2:
        return False, "⚠️ Language name must be at least 2 characters long."
    
    if len(language) > 100:
        return False, "⚠️ Language name is too long."
    
    # Check for suspicious patterns
    if re.search(r'[<>"\']', language):
        return False, "⚠️ Language name contains invalid characters."
    
    return True, "Valid language input."

def validate_custom_prompt(prompt: str) -> Tuple[bool, str]:
    """Validate custom prompt for summary extension"""
    if not prompt or not isinstance(prompt, str):
        return False, "⚠️ Custom prompt is required and must be a string."
    
    if len(prompt.strip()) < 5:
        return False, "⚠️ Custom prompt must be at least 5 characters long."
    
    if len(prompt) > 500:
        return False, "⚠️ Custom prompt is too long. Maximum 500 characters allowed."
    
    # Check for meaningful content
    if len(prompt.strip()) < 5:
        return False, "⚠️ Custom prompt must contain meaningful content."
    
    return True, "Valid custom prompt."

def get_file_type_info(file_path: str) -> dict:
    """Get detailed information about a file"""
    try:
        stat = os.stat(file_path)
        _, ext = os.path.splitext(file_path.lower())
        
        return {
            "size": stat.st_size,
            "extension": ext,
            "is_text": ext in SUPPORTED_TEXT_EXTENSIONS,
            "is_media": ext in SUPPORTED_MEDIA_EXTENSIONS,
            "size_mb": round(stat.st_size / (1024 * 1024), 2)
        }
    except OSError:
        return {"error": "Cannot access file"}

def estimate_processing_time(file_path: str) -> str:
    """Estimate processing time based on file characteristics"""
    info = get_file_type_info(file_path)
    if "error" in info:
        return "Unknown"
    
    size_mb = info["size_mb"]
    
    if info["is_text"]:
        if size_mb < 1:
            return "~5-10 seconds"
        elif size_mb < 5:
            return "~10-30 seconds"
        else:
            return "~30-60 seconds"
    elif info["is_media"]:
        if size_mb < 10:
            return "~30-60 seconds"
        elif size_mb < 50:
            return "~1-3 minutes"
        else:
            return "~3-5 minutes"
    
    return "Unknown"
