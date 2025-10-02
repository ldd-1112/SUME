"""
AI Services module for SUME Smart Summarizer
Handles text summarization, extension, and translation using Google Gemini
"""
from .config import model
from .cache_manager import cache_result
from .file_reader import extract_text_from_file, chunk_text

# --- Summarize, Extend, Translate ---
@cache_result
def summarize_text(input_text: str) -> str:
    """Summarize input text using Google Gemini"""
    try:
        resp = model.generate_content(f"Summarize the following text:\n\n{input_text}")
        return resp.text.strip() if resp and resp.text else "⚠️ Summarization failed."
    except Exception as e:
        return f"⚠️ Summarization error: {e}"

def summarize_file(file_path):
    """Summarize a file by processing it in chunks"""
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
    """Extend a summary with more details"""
    try:
        resp = model.generate_content(f"Expand the following summary into more details:\n\n{summary_text}")
        return resp.text.strip() if resp and resp.text else "⚠️ Could not extend summary."
    except Exception as e:
        return f"⚠️ Extend summary error: {e}"

@cache_result
def extend_summary_custom(summary_text: str, custom_prompt: str) -> str:
    """Extend a summary with custom focus areas"""
    try:
        prompt = f"Expand the following summary with specific focus on: {custom_prompt}\n\nSummary:\n{summary_text}"
        resp = model.generate_content(prompt)
        return resp.text.strip() if resp and resp.text else "⚠️ Could not extend summary with custom details."
    except Exception as e:
        return f"⚠️ Custom extend summary error: {e}"

@cache_result
def translate_text(summary_text: str, target_lang: str) -> str:
    """Translate text to target language"""
    try:
        resp = model.generate_content(f"Translate the following text into {target_lang}:\n\n{summary_text}")
        return resp.text.strip() if resp and resp.text else "⚠️ Translation failed."
    except Exception as e:
        return f"⚠️ Translation error: {e}"
