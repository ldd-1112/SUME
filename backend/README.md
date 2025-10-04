# SUME Backend

This directory contains the backend modules for the SUME (Smart Summarizer) application. The backend handles AI services, file processing, media handling, web scraping, and caching functionality.

## Architecture

The backend is organized into modular components that work together to provide comprehensive text summarization and translation capabilities.

## Modules

### Core AI Services (`ai_services.py`)
Handles all AI-powered operations using Google Gemini API.

**Functions:**
- `summarize_text(input_text: str) -> str` - Summarize input text using Gemini
- `summarize_file(file_path) -> str` - Summarize files by processing in chunks
- `extend_summary(summary_text: str) -> str` - Expand summary with more details
- `extend_summary_custom(summary_text: str, custom_prompt: str) -> str` - Extend summary with custom focus areas
- `translate_text(summary_text: str, target_lang: str) -> str` - Translate text to target language

**Features:**
- Caching enabled for all functions to improve performance
- Error handling with user-friendly messages
- Chunked processing for large files

### Configuration (`config.py`)
Manages API configuration and environment variables.

**Features:**
- Google Gemini API configuration
- Whisper model initialization for speech recognition
- Environment variable management
- Secure API key handling

### File Processing (`file_reader.py`)
Handles various file format processing and text extraction.

**Supported Formats:**
- `.txt` - Plain text files
- `.md` - Markdown files
- `.docx` - Microsoft Word documents
- `.pdf` - PDF documents

**Functions:**
- `extract_text_from_file(file_path: str) -> str` - Extract text from various file formats
- `chunk_text(text: str, max_chunk_size: int = 4000) -> List[str]` - Split large texts into manageable chunks

### Media Processing (`media_processor.py`)
Handles audio and video file processing for transcription.

**Features:**
- Speech-to-text conversion using Whisper
- Support for various audio/video formats
- URL-based media processing
- Error handling and validation

**Functions:**
- `speech_to_text(file_path: str) -> str` - Convert audio/video to text
- `transcribe_media_url(url: str) -> str` - Transcribe media from URL

### Web Scraping (`web_scraper.py`)
Extracts text content from web pages and media URLs.

**Functions:**
- `get_text_from_url(url: str, content_type: str) -> str` - Extract text from web pages or media URLs

**Features:**
- Handles various content types (web pages, media)
- Error handling for invalid URLs
- Content validation

### Caching (`cache_manager.py`)
Implements intelligent caching system to improve performance and reduce API costs.

**Features:**
- Function result caching using decorators
- Cache statistics and management
- Memory-efficient storage
- Cache clearing functionality

**Functions:**
- `cache_result` - Decorator for caching function results
- `clear_cache() -> str` - Clear all cached results
- `get_cache_stats() -> str` - Get cache statistics
- `get_cache_info() -> dict` - Get detailed cache information

### Input Validation (`validation.py`)
Comprehensive input validation system to ensure data quality and prevent unnecessary processing.

**Features:**
- Text input validation with length and content checks
- File validation for size, format, and existence
- URL validation for web content and media
- Language and custom prompt validation
- Processing time estimation
- File type information extraction

**Functions:**
- `validate_text_input(text: str) -> Tuple[bool, str]` - Validate text input for summarization
- `validate_file_input(file_path: str) -> Tuple[bool, str, Optional[str]]` - Validate file input for processing
- `validate_media_file(file_path: str) -> Tuple[bool, str, Optional[str]]` - Validate media files for transcription
- `validate_url(url: str, content_type: str = "web") -> Tuple[bool, str]` - Validate URLs for web scraping or media processing
- `validate_language(language: str) -> Tuple[bool, str]` - Validate language selection for translation
- `validate_custom_prompt(prompt: str) -> Tuple[bool, str]` - Validate custom extension prompts
- `estimate_processing_time(file_size: int, content_type: str) -> str` - Estimate processing time for files
- `get_file_type_info(file_path: str) -> Tuple[str, str, int]` - Get file type, extension, and size information

**Validation Rules:**
- Text: 10 characters minimum, 1M characters maximum
- Files: 50MB maximum size
- URLs: Valid format and accessible
- Languages: Must be in supported languages list

### Language Support (`languages.py`)
Centralized language list for translation features.

**Features:**
- Alphabetically sorted language list
- Support for 80+ languages
- Custom language input support
- Gemini API compatible

**Exported:**
- `languages_list` - Complete list of supported languages

## Dependencies

- `google-generativeai` - Google Gemini AI API
- `whisper` - OpenAI Whisper for speech recognition
- `python-docx` - Microsoft Word document processing
- `PyPDF2` - PDF document processing
- `requests` - HTTP requests for web scraping
- `python-dotenv` - Environment variable management

## Environment Variables

Create a `.env` file in the project root with:

```env
GOOGLE_API_KEY=your_gemini_api_key
GOOGLE_APPLICATION_CREDENTIALS=path_to_service_account_json
```

## Usage

The backend modules are designed to be imported and used by the main application:

```python
from backend import (
    summarize_text, 
    extend_summary, 
    translate_text, 
    languages_list,
    clear_cache,
    get_cache_info,
    validate_text_input,
    validate_file_input,
    validate_url
)

# Validate input before processing
is_valid, message = validate_text_input("Your text here...")
if is_valid:
    # Summarize text
    summary = summarize_text("Your text here...")
    
    # Translate to a specific language
    translation = translate_text(summary, "Spanish")

# Get available languages
print(languages_list)

# Get cache information
cache_info = get_cache_info()
print(f"Cache entries: {cache_info['total_entries']}")
```

## Error Handling

All functions include comprehensive error handling:
- API failures return user-friendly error messages
- File processing errors are caught and reported
- Network issues are handled gracefully
- Invalid inputs are validated and reported

## Performance Features

- **Caching**: All AI operations are cached to reduce API calls
- **Chunking**: Large files are processed in chunks to avoid token limits
- **Async Support**: Functions are designed to work with async frameworks
- **Memory Management**: Efficient memory usage for large file processing

## Contributing

When adding new functionality:
1. Follow the existing module structure
2. Add comprehensive error handling
3. Include caching where appropriate
4. Update this README with new functions
5. Add type hints for better code documentation

## License

This project is part of the SUME Smart Summarizer application.
