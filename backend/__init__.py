# Backend package for SUME Smart Summarizer
from .ai_services import summarize_text, extend_summary, extend_summary_custom, translate_text, summarize_file
from .languages import languages_list
from .media_processor import speech_to_text, transcribe_media_url
from .web_scraper import get_text_from_url
from .cache_manager import clear_cache, get_cache_stats, get_cache_info
from .validation import (
    validate_text_input, validate_file_input, validate_media_file, 
    validate_url, validate_language, validate_custom_prompt,
    estimate_processing_time, get_file_type_info
)

__all__ = [
    'summarize_text',
    'extend_summary', 
    'extend_summary_custom',
    'translate_text',
    'summarize_file',
    'speech_to_text',
    'transcribe_media_url',
    'get_text_from_url',
    'clear_cache',
    'get_cache_stats',
    'get_cache_info',
    'languages_list',
    'validate_text_input',
    'validate_file_input',
    'validate_media_file',
    'validate_url',
    'validate_language',
    'validate_custom_prompt',
    'estimate_processing_time',
    'get_file_type_info'
]
