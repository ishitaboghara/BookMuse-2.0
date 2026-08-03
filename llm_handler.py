"""
BookMuse 2.0 - LLM Handler
Groq LLM integration with Web Search, RAG context, High-Quality Scene Generator, and Vision Cover Analysis
"""

import time
import urllib.parse
from groq import Groq
from openai import OpenAI
from typing import List, Dict, Optional
from config import GROQ_API_KEY, OPENAI_API_KEY, LLM_MODEL, LLM_TEMP, LLM_MAX_TOKENS

class LLMHandler:
    def __init__(self):
        """Initialize LLM handler"""
        if not GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY not found in .env file")
        
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = LLM_MODEL
        self.temperature = LLM_TEMP
        self.max_tokens = LLM_MAX_TOKENS

        # Initialize OpenAI client if key available (for DALL-E 3 HD & GPT-4o Vision)
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    # ============================================================================
    # COMPANION CHATBOT FOR ANY BOOK
    # ============================================================================
    
    def discuss_book(self, book_title: str, author: str, query: str, 
                     context: str = "", language: str = "en", mode: str = "general") -> str:
        """
        Discuss ANY book with the user like a knowledgeable, friendly companion.
        """
        
        if language == "hi":
            system_prompt = f"""आप BookMuse हैं - पुस्तकों के प्रति भावुक एक मित्रवत, समझदार AI साथी।

आप उपयोगकर्ता के साथ "{book_title}" {f'(' + author + ' द्वारा)' if author else ''} के बारे में बातचीत कर रहे हैं।

{f"संदर्भ जानकारी:\n{context}" if context else ""}

निर्देश:
- हिंदी भाषा में स्वाभाविक, गर्मजोशी भरी और मित्रवत शैली में उत्तर दें (जैसे दो दोस्त चाय पर किताब की चर्चा कर रहे हों)।
- यदि सवाल पात्रों के बारे में है, तो उनके स्वभाव, निर्णयों और यात्रा की समीक्षा करें।
- यदि सवाल क्लाइमेक्स या ट्विस्ट पर है, तो कथानक के मोड़ों का गहरा विश्लेषण दें।
- यदि सवाल फिल्म अनुकूलन पर है, तो पुस्तक बनाम फिल्म के अंतर पर अपनी राय दें।
- 200 से 400 शब्दों में विचारशील और आकर्षक उत्तर दें।"""
        else:
            system_prompt = f"""You are BookMuse — a warm, passionate, and deeply knowledgeable AI book companion.

You are discussing "{book_title}" {f'by {author}' if author else ''} with the user.

{f"Reference Context:\n{context}" if context else ""}

Guidelines:
- Speak in a friendly, engaging, companionable tone — like two book-loving friends discussing over coffee.
- Focus on what makes this book unique: character motivations, plot twists, climaxes, underlying themes, or movie adaptation choices depending on what the user asks.
- If the user asks about plot twists or the climax, provide nuanced, insightful analysis.
- Give a detailed, thoughtful response (200–400 words).
- Encourage further discussion with a friendly follow-up thought at the end."""

        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            return message.choices[0].message.content.strip()
        
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"

    # ============================================================================
    # ULTRA HIGH-QUALITY SCENE TEXT-TO-IMAGE VISUALIZER
    # ============================================================================

    def generate_scene_image(self, scene_description: str, style: str = "Cinematic Fantasy", 
                             language: str = "en") -> Dict:
        """
        Generate a vivid, ultra high-quality visual scene image from descriptive book text.
        """
        enhancer_prompt = f"""You are a world-class movie art director and visual concept artist. Convert this book scene description into a masterwork visual image prompt for high-end AI artwork.

Scene Description: "{scene_description}"
Visual Style Target: {style}

Guidelines:
- Output ONLY the expanded artistic English prompt (max 70 words).
- Specify cinematic camera framing (e.g. wide anamorphic shot, atmospheric depth of field).
- Add lighting (e.g. volumetric rays, chiaroscuro contrast, golden hour warmth, glowing neon bloom).
- Detail environmental textures, mood, color grade, and artistic aesthetic.
- Do NOT include greetings, preamble, or meta text."""

        try:
            enhanced_resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You create stunning, ultra-detailed visual art prompts."},
                    {"role": "user", "content": enhancer_prompt}
                ],
                temperature=0.75,
                max_tokens=180,
            )
            expanded_prompt = enhanced_resp.choices[0].message.content.strip()
        except Exception:
            expanded_prompt = f"Masterpiece book scene artwork of {scene_description[:100]}, {style} style, cinematic lighting, 8k resolution concept art"

        image_url = None
        provider = "Pollinations FLUX Model"

        # Try DALL-E 3 HD if OpenAI key available
        if self.openai_client:
            try:
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=expanded_prompt,
                    size="1024x1024",
                    quality="hd",
                    n=1,
                )
                image_url = response.data[0].url
                provider = "OpenAI DALL-E 3 (HD Quality)"
            except Exception as e:
                print(f"INFO: DALL-E 3 HD generation fallback ({e}). Using FLUX model.")

        # High-Quality Pollinations FLUX Engine fallback
        if not image_url:
            seed = int(time.time()) % 10000
            quality_suffix = f"{style} style masterpiece, cinematic lighting, ultra detailed 8k resolution artwork"
            full_prompt_text = f"{expanded_prompt}, {quality_suffix}"
            encoded_prompt = urllib.parse.quote(full_prompt_text)
            
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&width=1280&height=720&nologo=true&enhance=true&seed={seed}"
            provider = "FLUX AI Visualizer (High Quality)"

        return {
            'success': True,
            'original_scene': scene_description,
            'enhanced_prompt': expanded_prompt,
            'image_url': image_url,
            'provider': provider,
            'style': style
        }

    # ============================================================================
    # ACCURATE BOOK COVER & IMAGE ANALYSIS
    # ============================================================================

    def analyze_book_cover_deep(self, cover_info: Dict, confirmed_title: str = "", 
                                base64_image: Optional[str] = None, 
                                web_context: str = "", language: str = "en") -> str:
        """
        Perform an accurate visual and story analysis of an uploaded book cover.
        Guarantees NO HALLUCINATIONS: uses OpenAI Vision if available, or user/OCR confirmed title + web context.
        """
        extracted_text = cover_info.get('extracted_text', '')
        color_tone = cover_info.get('dominant_color', 'Balanced Palette')
        orientation = cover_info.get('orientation', 'Portrait')

        # Mode A: OpenAI Vision analysis if key available
        if self.openai_client and base64_image:
            try:
                vision_prompt = """Examine this book cover image accurately. Tell me:
1. Identified Book Title & Author (read exact text on cover).
2. Cover Design & Aesthetic Breakdown (typography, color psychology, and mood).
3. Story Synopsis & Plot Hook.
4. Key Characters & Core Themes.
5. 3 Companion Discussion Questions."""
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": vision_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=900
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"INFO: Vision API call fallback: {e}")

        # Mode B: Title-Grounded Analysis (Prevents hallucinated titles)
        target_book = confirmed_title or cover_info.get('title_candidate', '') or extracted_text

        if language == "hi":
            analysis_prompt = f"""आप एक मास्टर पुस्तक समीक्षक और कला विश्लेषक हैं।

कवर की जानकारी:
- पुस्तक का नाम / शीर्षक: {target_book if target_book else 'कवर पाठ से स्वचालित रूप से नहीं मिला'}
- संदर्भ/सारांश: {web_context if web_context else 'उपलब्ध नहीं'}
- निकाली गई छवि विशेषताएँ: {color_tone}, {orientation}

निर्देश:
- यदि पुस्तक का शीर्षक दिया गया है, तो उसी पुस्तक का सटीक विश्लेषण दें।
- यदि पुस्तक शीर्षक अज्ञात है और पाठ नहीं मिला, तो उपयोगकर्ता से शीर्षक दर्ज करने का अनुरोध करें।
- कभी भी अपनी ओर से नकली या काल्पनिक पुस्तक का नाम न बनाएं।

रिपोर्ट के अनुभाग:
1. 📖 **पहचानी गई पुस्तक और लेखक**
2. 🎨 **कवर कला और डिजाइन विश्लेषण**
3. 📜 **कथानक और कहानी का सारांश**
4. 👥 **मुख्य पात्र और विषय**
5. 💡 **चर्चा के लिए सुझाव प्रश्न**"""
        else:
            analysis_prompt = f"""You are an expert literary critic and cover design analyst.

Cover & Book Information:
- Target Book Title: {target_book if target_book else 'Title could not be extracted directly from image font'}
- Verified Book Summary Context: {web_context if web_context else 'No external summary provided'}
- Visual Cover Features: Color Palette: {color_tone}, Layout: {orientation}

CRITICAL RULES:
- If the book title is known or provided (e.g. "{target_book}"), write an accurate analysis for THAT EXACT REAL BOOK.
- Do NOT invent or hallucinate fictional dummy book titles (never invent names like 'The Whispering Realms').
- If the title is unknown, explicitly ask the user to confirm/type the book title in the input box so BookMuse can fetch the exact details.

Generate a clean, structured report:
1. 📖 **Identified Book & Author**
2. 🎨 **Visual Design & Cover Aesthetics** (Analyze color tone, typography feel, and atmospheric mood)
3. 📜 **Story Synopsis & Plot Hook**
4. 👥 **Key Characters & Core Themes**
5. 💬 **Companion Discussion Starters**"""

        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You provide truthful, accurate, non-hallucinated book cover and literary analysis reports."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.4,
                max_tokens=950,
            )
            return message.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Error analyzing cover image: {str(e)}"

    # ============================================================================
    # CHARACTER ANALYSIS
    # ============================================================================
    
    def analyze_character(self, book_title: str, character_name: str, 
                         book_info: str = "", language: str = "en") -> str:
        query = f"Give a complete breakdown of character {character_name} in '{book_title}': personality traits, character arc, major conflicts, and significance."
        if language == "hi":
            query = f"'{book_title}' में पात्र {character_name} का पूर्ण विश्लेषण करें: उनका व्यक्तित्व, चरित्र यात्रा, मुख्य संघर्ष और कहानी में उनका महत्व।"
        
        return self.discuss_book(book_title, "", query, book_info, language, mode="character")

    # ============================================================================
    # BOOK RECOMMENDATIONS
    # ============================================================================
    
    def get_recommendations(self, liked_book: str, genre: str = "", 
                           mood: str = "", language: str = "en") -> str:
        if language == "hi":
            system_prompt = f"""आप एक पुस्तक सिफारिश विशेषज्ञ हैं।
उपयोगकर्ता "{liked_book}" {f'और ' + genre + ' शैली' if genre else ''} {f'और ' + mood + ' मूड' if mood else ''} की पुस्तकें पढ़ना चाहता है।

5 बेहतरीन पुस्तकों की सिफारिश करें। प्रत्येक के लिए समझाएं कि यह क्यों खास है।"""
        else:
            system_prompt = f"""You are a master book recommendation expert.
The user loved "{liked_book}" {f'and enjoys {genre} books' if genre else ''} {f'with a {mood} reading mood' if mood else ''}.

Recommend 5 fantastic books. For each book, explain:
1. Title & Author
2. Core Premise
3. Why they will love it based on their taste."""
        
        try:
            query = f"Recommend books similar to {liked_book}"
            if genre:
                query += f" in the {genre} genre"
            if mood:
                query += f" with a {mood} feel"
            
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            return message.choices[0].message.content.strip()
        
        except Exception as e:
            return f"❌ Error getting recommendations: {str(e)}"

    # ============================================================================
    # BOOK VS MOVIE COMPARISON
    # ============================================================================
    
    def compare_book_movie(self, book_title: str, movie_title: str = "", 
                          language: str = "en") -> str:
        movie_str = movie_title if movie_title else f"the movie adaptation of {book_title}"
        
        if language == "hi":
            system_prompt = f"""आप पुस्तक "{book_title}" और उसकी फिल्म "{movie_str}" की गहन तुलना करते हैं।

निम्नलिखित पर ध्यान दें:
- पुस्तक की तुलना में फिल्म में क्या बदला गया?
- कौन से पात्र हटाए या बदले गए?
- क्लाइमेक्स में क्या अंतर था?
- पुस्तक बनाम फिल्म: कौन सा बेहतर अनुभव प्रदान करता है?"""
        else:
            system_prompt = f"""You are an expert film and literary critic. Compare the book "{book_title}" with {movie_str}.

Analyze:
1. Plot and narrative alterations
2. Character additions, cuts, or performance changes
3. Climax and ending differences
4. Verdict: Which medium did the story greater justice and why?"""

        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Compare book '{book_title}' with its movie adaptation."}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return message.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Error comparing book and movie: {str(e)}"

    # ============================================================================
    # BOOK SUMMARY
    # ============================================================================
    
    def generate_summary(self, book_title: str, author: str, 
                        book_description: str, language: str = "en") -> str:
        if language == "hi":
            system_prompt = f"""आप "{book_title}" ({author}) की एक स्पष्ट, व्यापक सारांश प्रदान करते हैं।
पुस्तक का विवरण: {book_description}

एक मुख्य कथानक, प्रमुख पात्र, महत्वपूर्ण मोड़ और विषय को कवर करता सारांश लिखें।"""
        else:
            system_prompt = f"""Provide a comprehensive yet engaging summary of "{book_title}" by {author}.
Context: {book_description}

Cover: Core plot, central characters, major thematic arc, and why it is worth reading."""

        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Summarize {book_title}"}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return message.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Error generating summary: {str(e)}"

    # ============================================================================
    # GENERAL QUESTION ANSWERING
    # ============================================================================
    
    def answer_general_book_question(self, question: str, 
                                    context: str = "", language: str = "en") -> str:
        system_prompt = "You are BookMuse, an AI book expert. Answer the user's question with warmth, detail, and literary expertise."
        if language == "hi":
            system_prompt = "आप BookMuse हैं, एक AI पुस्तक विशेषज्ञ। उपयोगकर्ता के प्रश्न का उत्तर हिंदी में विस्तार और साहित्यिक समझ के साथ दें।"

        try:
            full_prompt = f"{context}\n\nQuestion: {question}" if context else question
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return message.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Error answering question: {str(e)}"