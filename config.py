"""
BookMuse 2.0 - Configuration
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load .env only for local development
load_dotenv()

# Read from Streamlit Secrets first, otherwise from .env
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

if not GROQ_API_KEY:
    print("⚠️ WARNING: GROQ_API_KEY not found")
    
# LLM Config
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMP = 0.7
LLM_MAX_TOKENS = 2048

# Voice Config
VOICE_LANGUAGES = ["en-US", "hi-IN"]

# Image Config
IMAGE_MODEL = "dall-e-3"
IMAGE_SIZE = "1024x1024"

# Embedding Config
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Genre Categories
GENRES = [
    "Mystery",
    "Romance",
    "Science Fiction",
    "Fantasy",
    "Thriller",
    "Historical Fiction",
    "Self-Help",
    "Memoir",
    "Comedy",
    "Drama",
    "Horror",
    "Adventure",
]

# Supported Languages
LANGUAGES = {
    "English": "en-US",
    "Hindi": "hi-IN",
}