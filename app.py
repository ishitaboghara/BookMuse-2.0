"""
BookMuse 2.0 - Complete Application
Main Streamlit UI with Companion Chatbot, Ultra-Quality Scene Visualizer,
Dedicated Send Voice Message Button, Deep Book Cover Analysis Report,
Bilingual Support (English & Hindi), and Book vs Movie Comparisons.
"""

import warnings
warnings.filterwarnings('ignore')
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import traceback
import tempfile
import streamlit as st
from dotenv import load_dotenv

# CRITICAL: Set page config FIRST
st.set_page_config(
    page_title="📚 BookMuse 2.0 - AI Book Companion",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

from book_handler import BookHandler
from web_search import BookSearcher
from ocr_processor import OCRProcessor
from genre_system import GenreSystem
from movie_comparison import MovieComparison
from llm_handler import LLMHandler
from voice_handler import VoiceHandler
from rag_engine import RAGEngine
import config

# Custom CSS for modern bookish aesthetic
st.markdown("""
    <style>
    .header { 
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4c1d95 70%, #701a75 100%); 
        color: white; 
        padding: 24px; 
        border-radius: 14px; 
        margin-bottom: 24px; 
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .user-message { 
        background-color: #eef2ff; 
        padding: 14px 18px; 
        border-radius: 12px; 
        margin: 10px 0; 
        border-left: 5px solid #4f46e5;
        color: #1e1b4b;
        font-size: 1.02em;
    }
    .bot-message { 
        background-color: #faf5ff; 
        padding: 16px 20px; 
        border-radius: 12px; 
        margin: 10px 0; 
        border-left: 5px solid #9333ea;
        color: #3b0764;
        font-size: 1.02em;
        line-height: 1.6;
    }
    .analysis-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e7ff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin: 12px 0;
    }
    .badge {
        background-color: #f3e8ff;
        color: #6b21a8;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85em;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'handlers_initialized' not in st.session_state:
    st.session_state.handlers_initialized = False

if 'current_book' not in st.session_state:
    st.session_state.current_book = "The Great Gatsby"

if 'search_results' not in st.session_state:
    st.session_state.search_results = None

if 'language' not in st.session_state:
    st.session_state.language = "English"

if 'voice_output_enabled' not in st.session_state:
    st.session_state.voice_output_enabled = True

if 'voice_input_enabled' not in st.session_state:
    st.session_state.voice_input_enabled = True

if 'cover_info' not in st.session_state:
    st.session_state.cover_info = {}

# ============================================================================
# INITIALIZE HANDLERS (ONCE)
# ============================================================================

if not st.session_state.handlers_initialized:
    try:
        with st.spinner("🔄 Initializing BookMuse 2.0..."):
            st.session_state.books_db = BookHandler()
            st.session_state.web_search = BookSearcher()
            st.session_state.ocr = OCRProcessor()
            st.session_state.genre_system = GenreSystem(st.session_state.books_db)
            st.session_state.movie_comp = MovieComparison(st.session_state.books_db)
            st.session_state.llm = LLMHandler()
            st.session_state.voice = VoiceHandler()
            st.session_state.rag = RAGEngine(st.session_state.books_db)
            st.session_state.handlers_initialized = True
    except Exception as e:
        st.error(f"Initialization Error: {e}")
        traceback.print_exc()
        st.stop()

# Helper for current language code
lang_code = "hi" if st.session_state.language == "Hindi" else "en"
sr_lang_code = "hi-IN" if st.session_state.language == "Hindi" else "en-US"

# Helper for executing companion chat query
def process_chat_query(query_text: str):
    if not query_text or not query_text.strip():
        return
    
    st.session_state.messages.append({'type': 'user', 'content': query_text})
    
    with st.spinner("🤔 BookMuse is thinking..."):
        try:
            context_str = ""
            local_books = st.session_state.books_db.search_books(st.session_state.current_book)
            if local_books:
                context_str = st.session_state.rag.build_context(query_text, local_books[0]['id'], k=3)
            else:
                search_res = st.session_state.web_search.get_wikipedia_info(st.session_state.current_book)
                if search_res.get('success'):
                    context_str = f"Summary: {search_res.get('full_summary', '')}"
                    st.session_state.rag.add_web_passages(st.session_state.current_book, [context_str])

            bot_response = st.session_state.llm.discuss_book(
                book_title=st.session_state.current_book,
                author="",
                query=query_text,
                context=context_str,
                language=lang_code
            )

            audio_path = None
            if st.session_state.voice_output_enabled:
                audio_path = st.session_state.voice.generate_tts_audio(bot_response, lang_code)

            st.session_state.messages.append({
                'type': 'bot',
                'content': bot_response,
                'audio_path': audio_path
            })
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error generating response: {e}")

# ============================================================================
# HEADER & SIDEBAR
# ============================================================================

st.markdown("""
<div class="header">
    <h1>📚 BookMuse 2.0</h1>
    <p>Your Multimodal AI Companion — Talk about ANY book, visualize scenes, listen to responses, and analyze cover art!</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400", use_container_width=True)
    st.markdown("### ⚙️ Preferences")
    
    st.session_state.language = st.radio(
        "🌐 Language / भाषा:",
        ["English", "Hindi"],
        index=0 if st.session_state.language == "English" else 1
    )
    
    st.session_state.voice_output_enabled = st.checkbox(
        "🔊 Voice Response Audio (gTTS)",
        value=st.session_state.voice_output_enabled
    )
    
    st.session_state.voice_input_enabled = st.checkbox(
        "🎤 Microphone Voice Input",
        value=st.session_state.voice_input_enabled
    )
    
    st.markdown("---")
    st.markdown("### 📖 Active Companion Book")
    active_book_input = st.text_input(
        "Discussing Book:",
        value=st.session_state.current_book,
        key="sidebar_book_name"
    )
    if active_book_input != st.session_state.current_book:
        st.session_state.current_book = active_book_input

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================================================
# MAIN NAVIGATION TABS
# ============================================================================

main_tabs = st.tabs([
    "💬 AI Companion Chat",
    "📸 Analyze Book Cover",
    "🎨 Scene Visualizer",
    "🔍 Search ANY Book",
    "🎯 Recommendations",
    "🎬 Book vs Movie",
    "🎭 Genres & Flashcards",
    "⚙️ Settings"
])

# ============================================================================
# TAB 1: AI BOOK COMPANION (CHATBOT)
# ============================================================================

with main_tabs[0]:
    st.markdown(f"### 💬 Chat with BookMuse about **'{st.session_state.current_book}'** (or ANY Book!)")
    st.markdown("Ask anything: characters, plot twists, climax explanations, theme analysis, or movie comparisons — like talking to a friend.")

    col_b1, col_b2 = st.columns([3, 1])
    with col_b1:
        target_book = st.text_input("📖 Current Book Title:", value=st.session_state.current_book)
        if target_book != st.session_state.current_book:
            st.session_state.current_book = target_book
    with col_b2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<span class='badge'>Language: {st.session_state.language}</span>", unsafe_allow_html=True)

    # Quick prompt shortcut buttons
    st.markdown("**Quick Discussion Starters:**")
    qs_col1, qs_col2, qs_col3, qs_col4 = st.columns(4)
    with qs_col1:
        if st.button("🎭 Main Characters"):
            process_chat_query(f"Who are the main characters in '{st.session_state.current_book}' and how do they develop?")
    with qs_col2:
        if st.button("⚡ Climax & Twists"):
            process_chat_query(f"What is the climax and biggest plot twist in '{st.session_state.current_book}'?")
    with qs_col3:
        if st.button("🎬 Book vs Movie"):
            process_chat_query(f"How does '{st.session_state.current_book}' compare to its movie adaptation?")
    with qs_col4:
        if st.button("💡 Themes & Meaning"):
            process_chat_query(f"What are the central themes and hidden meanings in '{st.session_state.current_book}'?")

    st.markdown("---")

    # Display Chat History
    for msg in st.session_state.messages:
        if msg['type'] == 'user':
            st.markdown(f'<div class="user-message"><b>👤 You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message"><b>📚 BookMuse:</b> {msg["content"]}</div>', unsafe_allow_html=True)
            if 'audio_path' in msg and msg['audio_path'] and os.path.exists(msg['audio_path']):
                st.audio(msg['audio_path'], format="audio/mp3")

    # Voice Input Section with DEDICATED SEND BUTTON
    if st.session_state.voice_input_enabled:
        st.markdown("#### 🎤 Voice Input (Speak instead of typing)")
        audio_data = st.audio_input("Record your voice message:")
        if audio_data is not None:
            with st.spinner("🔄 Transcribing your voice audio..."):
                transcribed_text = st.session_state.voice.transcribe_audio_file(audio_data, sr_lang_code)
                if transcribed_text:
                    st.success(f"🗣️ **Recognized Speech:** \"{transcribed_text}\"")
                    if st.button("🎤 Send Recorded Voice Message", type="primary", use_container_width=True):
                        process_chat_query(transcribed_text)
                else:
                    st.warning("⚠️ Could not recognize speech. Please try speaking clearly near your microphone.")

    st.markdown("---")

    # Text Input Section
    with st.form("chat_text_form", clear_on_submit=True):
        user_input = st.text_area(
            "Type your question:",
            placeholder=f"Ask anything about '{st.session_state.current_book}'...",
            height=90
        )
        send_submitted = st.form_submit_button("📤 Send Message", use_container_width=True, type="primary")

    if send_submitted and user_input.strip():
        process_chat_query(user_input.strip())

# ============================================================================
# TAB 2: ANALYZE BOOK COVER IMAGE (DEEP COVER REPORT)
# ============================================================================

with main_tabs[1]:
    st.markdown("### 📸 Analyze Book Cover & Get Complete Insights")
    st.markdown("Upload a photo of any book cover image to get a full analysis of the cover art, title, plot, themes, and characters!")

    uploaded_img = st.file_uploader("📷 Choose a book cover image (JPG, PNG):", type=['jpg', 'jpeg', 'png'])

    if uploaded_img:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp.write(uploaded_img.getbuffer())
            temp_img_path = tmp.name

        img_col1, img_col2 = st.columns([1, 2])
        with img_col1:
            st.image(uploaded_img, caption="Uploaded Book Cover", use_container_width=True)
            
            # Optional user title entry if font is stylized
            custom_title = st.text_input(
                "📖 Book Title (if stylized / ornate font):",
                placeholder="e.g. The Palace of Illusions",
                help="Type or confirm the book title here to fetch 100% accurate plot & character details!"
            )
            analyze_cover_btn = st.button("🔍 Generate Deep Cover & Story Report", type="primary", use_container_width=True)

        with img_col2:
            if analyze_cover_btn or 'last_cover_report' not in st.session_state:
                with st.spinner("🔍 Analyzing cover visual design, title, plot, and themes..."):
                    cover_info = st.session_state.ocr.get_book_info_from_image(temp_img_path)
                    st.session_state.cover_info = cover_info
                    
                    target_title = custom_title.strip() or cover_info.get('title_candidate') or ""
                    
                    # Fetch real web context for accuracy if title is known
                    web_ctx = ""
                    if target_title:
                        search_res = st.session_state.web_search.get_wikipedia_info(target_title)
                        if search_res.get('success'):
                            web_ctx = search_res.get('full_summary', '')
                        else:
                            gb_res = st.session_state.web_search.get_google_books_info(target_title)
                            if gb_res.get('success'):
                                web_ctx = gb_res.get('full_description', '')

                    b64_img = st.session_state.ocr.encode_image_base64(temp_img_path)
                    
                    report = st.session_state.llm.analyze_book_cover_deep(
                        cover_info=cover_info,
                        confirmed_title=target_title,
                        base64_image=b64_img,
                        web_context=web_ctx,
                        language=lang_code
                    )
                    st.session_state.last_cover_report = report
                    st.session_state.last_analyzed_title = target_title

            if 'last_cover_report' in st.session_state:
                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                st.markdown(st.session_state.last_cover_report)
                st.markdown('</div>', unsafe_allow_html=True)

                if st.button("💬 Discuss This Book with Companion", type="secondary"):
                    chosen_title = st.session_state.get('last_analyzed_title') or st.session_state.cover_info.get('title_candidate') or "The Palace of Illusions"
                    if chosen_title:
                        st.session_state.current_book = chosen_title
                    st.rerun()

        try:
            os.remove(temp_img_path)
        except Exception:
            pass

# ============================================================================
# TAB 3: SCENE TEXT-TO-IMAGE VISUALIZER
# ============================================================================

with main_tabs[2]:
    st.markdown("### 🎨 High-Quality Scene Text-to-Image Visualizer")
    st.markdown("Describe any scene from a book in words, and AI will generate stunning artwork for you!")

    col1, col2 = st.columns([2, 1])
    with col1:
        scene_text = st.text_area(
            "📖 Book Scene Description:",
            placeholder="e.g. A grand medieval banquet hall with floating candles, tall stained glass windows reflecting moonlight, and ancient banners...",
            height=130
        )
    with col2:
        art_style = st.selectbox(
            "🎨 Visual Style:",
            ["Cinematic Fantasy", "Digital Illustration", "Oil Painting", "Anime Concept", "Photorealistic", "Dark Gothic Sketch"]
        )
        gen_btn = st.button("✨ Render Visual Scene", use_container_width=True, type="primary")

    if gen_btn and scene_text:
        with st.spinner("🎨 Creating high-resolution artwork of your book scene..."):
            try:
                res = st.session_state.llm.generate_scene_image(scene_text, style=art_style, language=lang_code)
                if res.get('success'):
                    st.success(f"✅ Rendered via **{res['provider']}**")
                    st.image(res['image_url'], caption=f"Visual Scene Artwork ({art_style})", use_container_width=True)
                    
                    with st.expander("🔍 Expanded Concept Art Prompt"):
                        st.write(f"**Expanded Prompt:** {res['enhanced_prompt']}")
                else:
                    st.error("Failed to generate scene image.")
            except Exception as e:
                st.error(f"Error generating image: {e}")

# ============================================================================
# TAB 4: SEARCH ANY BOOK
# ============================================================================

with main_tabs[3]:
    st.markdown("### 🔍 Search ANY Book in the World")
    st.markdown("Fetches plot summary, metadata, author info, and Goodreads/Wikipedia details for any book.")

    s_col1, s_col2 = st.columns([3, 1])
    with s_col1:
        sq = st.text_input("📚 Book Title or Author:", placeholder="e.g. Dune, Crime and Punishment, Atomic Habits")
    with s_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        s_btn = st.button("🔍 Search Online", use_container_width=True)

    if s_btn and sq:
        with st.spinner(f"🔍 Searching online databases for '{sq}'..."):
            res = st.session_state.web_search.search_book_complete(sq)
            st.session_state.search_results = res

    if st.session_state.search_results:
        res = st.session_state.search_results
        combined = res.get('combined', {})
        st.markdown(f"## 📖 {res.get('book_title', 'Book Results')}")

        if combined.get('plot_summary'):
            st.markdown(f"**Plot Summary:** {combined['plot_summary']}")
        if combined.get('author_info'):
            st.markdown(f"**Author Details:** {combined['author_info']}")
        if combined.get('categories'):
            st.markdown(f"**Categories:** {', '.join(combined['categories'])}")

        if st.button("💬 Start Companion Discussion for This Book", type="primary"):
            st.session_state.current_book = res.get('book_title', sq)
            st.rerun()

# ============================================================================
# TAB 5: BOOK RECOMMENDATIONS
# ============================================================================

with main_tabs[4]:
    st.markdown("### 🎯 Personalized Book Recommendations")
    
    rec_col1, rec_col2, rec_col3 = st.columns(3)
    with rec_col1:
        rec_book = st.text_input("Book you liked:", value=st.session_state.current_book)
    with rec_col2:
        rec_genre = st.selectbox("Preferred Genre:", ["Any"] + config.GENRES)
    with rec_col3:
        rec_mood = st.selectbox("Reading Mood:", ["Fast-Paced & Thrilling", "Thought-Provoking & Deep", "Cozy & Heartwarming", "Dark & Mysterious", "Inspiring & Uplifting"])

    if st.button("✨ Get Recommendations", use_container_width=True, type="primary"):
        with st.spinner("🎯 Finding perfect book matches..."):
            genre_param = "" if rec_genre == "Any" else rec_genre
            recs = st.session_state.llm.get_recommendations(
                liked_book=rec_book,
                genre=genre_param,
                mood=rec_mood,
                language=lang_code
            )
            st.markdown(recs)

# ============================================================================
# TAB 6: BOOK VS MOVIE HUB
# ============================================================================

with main_tabs[5]:
    st.markdown("### 🎬 Book vs Movie Adaptation Hub")
    st.markdown("Compare plot, characters, climax modifications, and adaptation choices for any book turned into a film!")

    m_col1, m_col2 = st.columns([3, 1])
    with m_col1:
        movie_book_title = st.text_input("📖 Book Title:", value=st.session_state.current_book, key="movie_tab_book")
    with m_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        compare_btn = st.button("🎬 Compare Book & Movie", use_container_width=True, type="primary")

    if compare_btn and movie_book_title:
        with st.spinner(f"🎬 Analyzing adaptation of '{movie_book_title}'..."):
            comp_analysis = st.session_state.llm.compare_book_movie(movie_book_title, language=lang_code)
            st.markdown(comp_analysis)

# ============================================================================
# TAB 7: GENRES & FLASHCARDS
# ============================================================================

with main_tabs[6]:
    st.markdown("### 🎭 Genres & Flashcards")
    sel_genre = st.selectbox("📚 Select Genre:", config.GENRES)

    if sel_genre:
        stats = st.session_state.genre_system.get_genre_stats(sel_genre)
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            st.metric("Catalog Books", stats.get('book_count', 0))
        with fc2:
            st.metric("Avg Rating", f"{stats.get('average_rating', 'N/A')}/5")
        with fc3:
            st.metric("Flashcards", stats.get('flashcard_count', 0))

        st.markdown("---")
        cards = st.session_state.genre_system.get_genre_flashcards(sel_genre)
        if cards:
            st.markdown(f"#### 🎓 Trivia Flashcards ({len(cards)})")
            for i, card in enumerate(cards[:5], 1):
                with st.expander(f"Card {i}: {card.get('front', '')}"):
                    st.write(f"**Answer:** {card.get('back', '')}")

# ============================================================================
# TAB 8: SETTINGS
# ============================================================================

with main_tabs[7]:
    st.markdown("### ⚙️ System Settings & Diagnostics")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("#### 🌐 Primary Language")
        st.write(f"Current Selected: **{st.session_state.language}**")
        st.write("Supported: English, Hindi (हिंदी)")

    with col_s2:
        st.write("#### 🔊 Audio & Voice Options")
        st.write(f"Voice Output (gTTS MP3): **{'Enabled' if st.session_state.voice_output_enabled else 'Disabled'}**")
        st.write(f"Voice Input (st.audio_input): **{'Enabled' if st.session_state.voice_input_enabled else 'Disabled'}**")

    st.markdown("---")
    st.write("#### 📊 System Metadata")
    st.write(f"- Indexed RAG Passages: `{len(st.session_state.rag.passages)}`")
    st.write(f"- Catalog Books: `{len(st.session_state.books_db.get_all_books())}`")
    st.write(f"- Environment: `Python 3.12 | Streamlit Cloud Ready`")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.88em;">
    <p>📚 <b>BookMuse 2.0</b> — AI Book Companion & Multimodal Assistant</p>
    <p>Groq LLaMA 3.3 | FAISS RAG | gTTS Audio | FLUX Scene Generator</p>
</div>
""", unsafe_allow_html=True)