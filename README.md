# 📚 BookMuse - AI Book Companion

An intelligent AI application that lets you discuss ANY book in natural conversation. Ask questions about characters, themes, plot points - visualize scenes - hear everything read aloud. All in your preferred language.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🗣️ **Voice Interface**
- **Speak to Ask**: Ask questions using voice input (speech-to-text)
- **Hear Responses**: Get AI responses read aloud in natural voice
- **Multiple Languages**: English and Hindi support

### 📚 **Smart Book Discussions**
- Discuss ANY book in the world (not limited to pre-loaded books)
- Deep literary analysis using RAG (Retrieval-Augmented Generation)
- Explore characters, themes, plot, and symbolism
- Analyze life lessons and meanings
- Ask about endings and narrative structure

### 🔍 **Web Search Integration**
- Fetch book information from Wikipedia
- Get data from Google Books API
- Retrieve real-time information about any book

### 📸 **Image Processing**
- Upload book cover photos
- Extract text using OCR
- Identify books from images
- Get instant summaries

### 🎭 **Genre-Based Learning**
- Explore 12+ genres
- Interactive flashcards for each book
- Study guides and learning paths
- Genre statistics and recommendations

### 🎬 **Movie Comparisons**
- Compare books with movie adaptations
- Analyze differences in storytelling
- Understand adaptation choices
- Discussion prompts for both versions

### 📖 **Personalized Recommendations**
- Get book suggestions by genre
- Find similar books based on themes
- Cross-genre recommendations
- Top-rated books in any category

### 🧠 **Powered by Advanced AI**
- **LLM**: Groq LLaMA 3.3-70b for intelligent responses
- **RAG**: Semantic retrieval of relevant passages
- **Embeddings**: Deep understanding of literary content
- **Vector Search**: FAISS for instant passage retrieval

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key (free at https://console.groq.com)
- (Optional) OpenAI API Key for image generation

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/bookmuse.git
cd bookmuse
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys:
# GROQ_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here (optional)
```

5. **Run the application**
```bash
streamlit run app.py
```

6. **Open in browser**

Live Demo:
https://bookmuse-2.streamlit.app

## 👩‍💻 Author

**Ishita Boghara**

MCA Student

SNDT Women's University
