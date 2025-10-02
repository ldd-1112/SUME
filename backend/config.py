"""
Configuration module for SUME Smart Summarizer
Handles API configuration and environment variables
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure APIs securely
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize Whisper model for speech recognition
whisper_model = None

def get_whisper_model():
    """Get or initialize Whisper model"""
    global whisper_model
    if whisper_model is None:
        import whisper
        whisper_model = whisper.load_model("base")  # Using base model for speed
    return whisper_model
