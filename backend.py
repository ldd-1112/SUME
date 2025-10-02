import google.generativeai as genai
from pydub import AudioSegment
import yt_dlp
import whisper
import trafilatura
import requests
import urllib.parse
import tempfile
import os
import logging
import hashlib
import shutil
from functools import wraps 
from dotenv import load_dotenv
from file_reader import extract_text_from_file, chunk_text

# Load environment variables
load_dotenv()

# Configure APIs securely
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize Whisper model for speech recognition
whisper_model = None
def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        whisper_model = whisper.load_model("base")  # Using base model for speed
    return whisper_model

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

# --- Utility: Convert audio for Whisper ---
def prepare_audio_for_whisper(input_file: str) -> str:
    """Convert audio to format suitable for Whisper processing"""
    output_file = tempfile.mktemp(suffix=".wav")
    audio = AudioSegment.from_file(input_file)
    
    # Convert to mono and standardize sample rate
    audio = audio.set_frame_rate(16000).set_channels(1)
    
    # Export as WAV
    audio.export(output_file, format="wav")
    
    return output_file

# --- Speech-to-Text using Whisper ---
def speech_to_text(file_path: str) -> str:
    try:
        # Prepare audio for Whisper
        wav_file = prepare_audio_for_whisper(file_path)
        
        # Load Whisper model
        whisper_model = get_whisper_model()
        
        # Transcribe audio
        result = whisper_model.transcribe(wav_file)
        
        # Clean up temp file
        if os.path.exists(wav_file):
            os.remove(wav_file)
        
        # Return transcript
        transcript = result["text"].strip()
        return transcript if transcript else "⚠️ Could not recognize speech."
        
    except Exception as e:
        logging.error(f"Whisper speech-to-text error: {e}")
        return f"⚠️ Speech-to-text failed: {e}"

# --- Summarize, Extend, Translate ---
@cache_result
def summarize_text(input_text: str) -> str:
    try:
        resp = model.generate_content(f"Summarize the following text:\n\n{input_text}")
        return resp.text.strip() if resp and resp.text else "⚠️ Summarization failed."
    except Exception as e:
        return f"⚠️ Summarization error: {e}"
    
# --- Summarize file ---
def summarize_file(file_path):
    text = extract_text_from_file(file_path)
    if text.startswith("⚠️"):
        return text

    summaries = []
    for chunk in chunk_text(text):
        resp = model.generate_content(f"Summarize the following text:\n\n{chunk}")
        if resp and resp.text:
            summaries.append(resp.text.strip())

    if len(summaries) == 0:
        return "⚠️ Summarization failed."

    # Merge summaries if multiple chunks
    final_summary = "\n\n".join(summaries)
    return final_summary


@cache_result
def extend_summary(summary_text: str) -> str:
    try:
        resp = model.generate_content(f"Expand the following summary into more details:\n\n{summary_text}")
        return resp.text.strip() if resp and resp.text else "⚠️ Could not extend summary."
    except Exception as e:
        return f"⚠️ Extend summary error: {e}"

@cache_result
def extend_summary_custom(summary_text: str, custom_prompt: str) -> str:
    try:
        prompt = f"Expand the following summary with specific focus on: {custom_prompt}\n\nSummary:\n{summary_text}"
        resp = model.generate_content(prompt)
        return resp.text.strip() if resp and resp.text else "⚠️ Could not extend summary with custom details."
    except Exception as e:
        return f"⚠️ Custom extend summary error: {e}"

@cache_result
def translate_text(summary_text: str, target_lang: str) -> str:
    try:
        resp = model.generate_content(f"Translate the following text into {target_lang}:\n\n{summary_text}")
        return resp.text.strip() if resp and resp.text else "⚠️ Translation failed."
    except Exception as e:
        return f"⚠️ Translation error: {e}"

# --- URL Handling ---
@cache_result
def extract_article_main_text(url: str) -> str:
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
def download_audio_from_media_url(url: str) -> str:
    try:
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, "audio.mp3")

        # --- YouTube or other sites via yt-dlp ---
        if "youtube.com" in url or "youtu.be" in url:
            ydl_opts = {
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                "quiet": True,
                "no_warnings": True,
                "extract_flat": False,
                "socket_timeout": 30,
                "retries": 3,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Find the downloaded file (yt-dlp might rename it)
            downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith(('.mp3', '.m4a', '.webm'))]
            if downloaded_files:
                actual_file_path = os.path.join(temp_dir, downloaded_files[0])
                return actual_file_path
            else:
                return f"⚠️ No audio file found after download"

        # --- Direct media download ---
        else:
            ext = os.path.splitext(url)[-1].split("?")[0] or ".mp3"
            temp_file_path = os.path.join(temp_dir, f"audio{ext}")

            r = requests.get(url, stream=True, timeout=30)
            if r.status_code != 200:
                return f"⚠️ Could not download media file, HTTP {r.status_code}"

            with open(temp_file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return temp_file_path

    except Exception as e:
        return f"⚠️ Audio download error: {e}"


def transcribe_media_url(url: str) -> str:
    file_path = download_audio_from_media_url(url)
    if file_path.startswith("⚠️"):
        return file_path
    
    # Check if file actually exists
    if not os.path.exists(file_path):
        return f"⚠️ Downloaded file not found: {file_path}"
    
    try:
        transcript = speech_to_text(file_path)
        return transcript
    except Exception as e:
        return f"⚠️ Speech-to-text failed: {e}"
    finally:
        # Clean up the entire temp directory
        temp_dir = os.path.dirname(file_path)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

@cache_result
def get_text_from_url(url: str, source_type: str) -> str:
    if source_type == "Webpage":
        return extract_article_main_text(url)
    elif source_type == "Media":
        return transcribe_media_url(url)
    else:
        return "⚠️ Invalid source type."

# --- Cache Management ---
def clear_cache():
    """Clear the in-memory cache"""
    global cache
    cache.clear()
    return "Cache cleared successfully!"

def get_cache_stats():
    """Get cache statistics"""
    return f"Cache size: {len(cache)} items"
