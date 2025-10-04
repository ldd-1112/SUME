# SUME - Smart Summarizer

A powerful AI-powered text summarization tool built with Gradio and Google's Gemini AI. SUME can summarize text from multiple sources including direct input, files, web pages, and media content.

## Features

- **Text Summarization**: Summarize any text input using Google's Gemini AI
- **File Processing**: Support for TXT, MD, PDF, DOCX files
- **Web Content**: Extract and summarize web articles from URLs
- **Media Processing**: Audio/video transcription and summarization
- **Translation**: Multi-language support (English, Vietnamese, French, Spanish)
- **Custom Extensions**: Extend summaries with specific focus areas
- **Performance**: Built-in caching for faster processing

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- FFmpeg (for audio processing)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ldd-1112/SUME.git
cd SUME
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the project root:
```bash
# Create .env file
touch .env
# Edit .env with your API keys (see Configuration section below)
```

4. **Run the application:**
```bash
python app.py
```

5. **Open your browser** and go to `http://127.0.0.1:7860`

## ⚙️ Configuration

Create a `.env` file with your API keys:

```env
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=your_service_account_file.json
```

## Usage

### Text Summarization
1. **Direct Text**: Paste your text directly into the input field
2. **File Upload**: Upload documents (TXT, MD, PDF, DOCX)
3. **Web URL**: Enter a webpage URL to summarize
4. **Media URL**: Process YouTube videos or audio files

### Advanced Features
- **Quick Extend**: Automatically expand summaries with more details
- **Custom Extend**: Specify what details to focus on
- **Translation**: Translate summaries to multiple languages
- **Cache Management**: Clear cache and view statistics

### Screenshots
The application provides a clean, intuitive interface with:
- Tabbed interface for different input types
- Real-time processing indicators
- Easy-to-use controls for all features
- Responsive design that works on all devices

## Technical Details

- **Frontend**: Gradio with modern UI
- **AI Model**: Google Gemini 2.5 Flash
- **Speech-to-Text**: OpenAI Whisper
- **Web Scraping**: Trafilatura
- **Media Processing**: yt-dlp, pydub
- **File Processing**: PyPDF2, python-docx

## Project Structure

```
SUME/
├── app.py                 # Main Gradio application
├── backend/               # Backend modules
│   ├── __init__.py       # Package initialization
│   ├── config.py         # API and model configuration
│   ├── ai_services.py    # AI/ML services (summarization, translation)
│   ├── media_processor.py # Audio/video processing
│   ├── web_scraper.py    # Web content extraction
│   ├── cache_manager.py  # Caching functionality
│   ├── file_reader.py    # File processing utilities
│   ├── validation.py     # Input validation utilities
│   └── languages.py      # Language support definitions
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
└── README.md             # This file
```

## Requirements

- `google-generativeai` - Google Gemini AI
- `gradio` - Web interface
- `openai-whisper` - Speech recognition
- `trafilatura` - Web content extraction
- `yt-dlp` - Media downloading
- `pydub` - Audio processing
- `PyPDF2` - PDF processing
- `python-docx` - Word document processing
- `beautifulsoup4` - HTML parsing
- `python-dotenv` - Environment variables
- `requests` - HTTP requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini AI for powerful text processing
- Gradio for the beautiful web interface
- OpenAI Whisper for speech recognition
- All the open-source libraries that make this possible

---

**Made with ❤️ by ldd-1112**