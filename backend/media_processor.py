"""
Media Processing module for SUME Smart Summarizer
Handles audio/video processing and speech-to-text conversion with improved resource management
"""
import tempfile
import os
import logging
import shutil
import atexit
from contextlib import contextmanager
from pydub import AudioSegment
import yt_dlp
import requests
from .config import get_whisper_model
from .validation import validate_media_file, estimate_processing_time

# Global whisper model cache
_whisper_model = None
_temp_dirs = set()

def _cleanup_temp_dirs():
    """Clean up all temporary directories on exit"""
    for temp_dir in _temp_dirs.copy():
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        _temp_dirs.discard(temp_dir)

# Register cleanup function
atexit.register(_cleanup_temp_dirs)

@contextmanager
def temp_audio_file(suffix=".wav"):
    """Context manager for temporary audio files with automatic cleanup"""
    temp_file = None
    try:
        temp_file = tempfile.mktemp(suffix=suffix)
        yield temp_file
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)

def prepare_audio_for_whisper(input_file: str) -> str:
    """Convert audio to format suitable for Whisper processing with better error handling"""
    try:
        # Validate input file first
        is_valid, error_msg, ext = validate_media_file(input_file)
        if not is_valid:
            raise ValueError(error_msg)
        
        with temp_audio_file(".wav") as output_file:
            # Load audio with error handling
            try:
                audio = AudioSegment.from_file(input_file)
            except Exception as e:
                raise ValueError(f"Failed to load audio file: {e}")
            
            # Convert to mono and standardize sample rate
            try:
                audio = audio.set_frame_rate(16000).set_channels(1)
            except Exception as e:
                raise ValueError(f"Failed to process audio: {e}")
            
            # Export as WAV with error handling
            try:
                audio.export(output_file, format="wav")
            except Exception as e:
                raise ValueError(f"Failed to export audio: {e}")
            
            # Return a copy since the temp file will be cleaned up
            final_file = tempfile.mktemp(suffix=".wav")
            shutil.copy2(output_file, final_file)
            return final_file
            
    except Exception as e:
        logging.error(f"Audio preparation error: {e}")
        raise

def speech_to_text(file_path: str) -> str:
    """Convert speech to text using OpenAI Whisper with improved resource management"""
    wav_file = None
    try:
        # Validate input first
        is_valid, error_msg, ext = validate_media_file(file_path)
        if not is_valid:
            return error_msg
        
        # Get processing time estimate
        time_estimate = estimate_processing_time(file_path)
        logging.info(f"Processing media file, estimated time: {time_estimate}")
        
        # Prepare audio for Whisper
        wav_file = prepare_audio_for_whisper(file_path)
        
        # Use cached model or load new one
        global _whisper_model
        if _whisper_model is None:
            _whisper_model = get_whisper_model()
        
        # Transcribe audio with progress tracking
        logging.info("Starting transcription...")
        result = _whisper_model.transcribe(wav_file)
        
        # Return transcript
        transcript = result["text"].strip()
        if not transcript:
            return "⚠️ Could not recognize speech. The audio might be too quiet or unclear."
        
        logging.info(f"Transcription completed. Length: {len(transcript)} characters")
        return transcript
        
    except ValueError as e:
        # Input validation errors
        return str(e)
    except Exception as e:
        logging.error(f"Whisper speech-to-text error: {e}")
        return f"⚠️ Speech-to-text failed: {e}"
    finally:
        # Clean up temp file
        if wav_file and os.path.exists(wav_file):
            try:
                os.remove(wav_file)
            except OSError:
                logging.warning(f"Could not remove temp file: {wav_file}")

def download_audio_from_media_url(url: str) -> str:
    """Download audio from media URL (YouTube, direct links, etc.)"""
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
    """Download and transcribe media from URL"""
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
