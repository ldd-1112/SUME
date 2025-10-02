import os
import re
from PyPDF2 import PdfReader
from docx import Document
from bs4 import BeautifulSoup

# --- Extract text by file type ---
def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_md(file_path):
    text = extract_txt(file_path)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)  # remove code blocks
    text = re.sub(r"#+\s*", "", text)  # remove headers
    text = re.sub(r"(\*\*|__|\*|_)", "", text)  # remove bold/italic
    return text.strip()

def extract_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    return soup.get_text()

# --- Wrapper ---
def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return extract_txt(file_path)
    elif ext == ".md":
        return extract_md(file_path)
    elif ext == ".pdf":
        return extract_pdf(file_path)
    elif ext == ".docx":
        return extract_docx(file_path)
    elif ext in [".html", ".htm"]:
        return extract_html(file_path)
    else:
        return f"⚠️ Unsupported file type: {ext}"

# --- Chunk text if too long ---
def chunk_text(text, max_words=1000):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i+max_words])