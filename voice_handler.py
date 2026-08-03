"""
BookMuse 2.0 - Voice Handler
gTTS text-to-speech synthesis and Streamlit browser audio transcription
Production quality, Python 3.12 & Streamlit Cloud compatible
"""

import os
import io
import tempfile
from typing import Optional, Dict
from gtts import gTTS
import speech_recognition as sr

class VoiceHandler:
    def __init__(self):
        """Initialize voice handler"""
        self.recognizer = sr.Recognizer()
        
    # ============================================================================
    # TEXT TO SPEECH (gTTS)
    # ============================================================================
    
    def generate_tts_audio(self, text: str, language: str = "en") -> Optional[str]:
        """
        Convert text to speech using gTTS and save to a temporary MP3 file.
        
        Args:
            text: Text to synthesize
            language: "en" for English, "hi" for Hindi
        
        Returns:
            Path to generated MP3 file, or None if failed
        """
        if not text or not text.strip():
            return None
            
        try:
            lang_code = "hi" if language.lower() in ["hi", "hindi", "hi-in"] else "en"
            
            # Clean text formatting
            clean_text = text.replace("**", "").replace("*", "").replace("#", "").strip()
            if len(clean_text) > 3000:
                clean_text = clean_text[:3000] + "..."
                
            tts = gTTS(text=clean_text, lang=lang_code, slow=False)
            
            temp_dir = tempfile.gettempdir()
            filename = f"bookmuse_speech_{hash(clean_text[:50]) & 0xffffffff}.mp3"
            filepath = os.path.join(temp_dir, filename)
            
            tts.save(filepath)
            return filepath
            
        except Exception as e:
            print(f"ERROR: gTTS synthesis failed: {e}")
            return None

    # ============================================================================
    # SPEECH TO TEXT (From Audio Bytes / Upload / Browser Mic)
    # ============================================================================
    
    def transcribe_audio_file(self, audio_source, language_code: str = "en-US") -> Optional[str]:
        """
        Transcribe audio file or bytes from Streamlit audio input.
        
        Args:
            audio_source: File path, BytesIO object, or Streamlit UploadedFile
            language_code: "en-US" or "hi-IN"
        
        Returns:
            Transcribed text string or None
        """
        try:
            # Handle BytesIO / Streamlit UploadedFile
            if hasattr(audio_source, "read"):
                audio_bytes = audio_source.read()
                temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                temp_wav.write(audio_bytes)
                temp_wav.close()
                audio_path = temp_wav.name
            elif isinstance(audio_source, str):
                audio_path = audio_source
            else:
                return None
            
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                
            text = self.recognizer.recognize_google(audio_data, language=language_code)
            
            # Clean up temp file if created
            if hasattr(audio_source, "read") and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except Exception:
                    pass
                    
            return text
            
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"ERROR: Audio transcription failed: {e}")
            return None

    def get_language_code(self, language_name: str) -> str:
        """
        Convert language name to speech recognition language code
        """
        codes = {
            "English": "en-US",
            "Hindi": "hi-IN",
        }
        return codes.get(language_name, "en-US")

    def check_microphone_quality(self) -> Dict:
        """
        Check helper for UI compatibility
        """
        return {
            'ready': True,
            'message': 'Browser microphone support active via Streamlit audio recorder.'
        }