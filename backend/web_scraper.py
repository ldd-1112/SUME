"""
Web Scraping module for SUME Smart Summarizer
Handles URL processing and web content extraction
"""
import urllib.parse
import trafilatura
from .cache_manager import cache_result
from .media_processor import transcribe_media_url

@cache_result
def extract_article_main_text(url: str) -> str:
    """Extract main text content from a webpage URL"""
    try:
        if not urllib.parse.urlparse(url).scheme:
            url = "http://" + url
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return "⚠️ Could not download content from URL."
        text = trafilatura.extract(downloaded)
        return text if text else "⚠️ No main text found in the webpage."
    except Exception as e:
        return f"⚠️ Error extracting text: {e}"

@cache_result
def get_text_from_url(url: str, source_type: str) -> str:
    """Get text content from URL based on source type"""
    if source_type == "Webpage":
        return extract_article_main_text(url)
    elif source_type == "Media":
        return transcribe_media_url(url)
    else:
        return "⚠️ Invalid source type."
