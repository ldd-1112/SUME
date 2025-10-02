"""
Media Processing module for SUME Smart Summarizer
Handles audio/video processing and speech-to-text conversion
"""
import tempfile
import os
import logging
import shutil
from pydub import AudioSegment
import yt_dlp
import requests
from .config import get_whisper_model

def prepare_audio_for_whisper(input_file: str) -> str:
    """Convert audio to format suitable for Whisper processing"""
    output_file = tempfile.mktemp(suffix=".wav")
    audio = AudioSegment.from_file(input_file)
    
    # Convert to mono and standardize sample rate
    audio = audio.set_frame_rate(16000).set_channels(1)
    
    # Export as WAV
    audio.export(output_file, format="wav")
    
    return output_file

def speech_to_text(file_path: str) -> str:
    """Convert speech to text using OpenAI Whisper"""
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
