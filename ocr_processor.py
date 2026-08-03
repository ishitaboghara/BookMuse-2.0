"""
BookMuse 2.0 - OCR & Vision Cover Processor
Extracts text, visual palette features, and identifies book metadata with fallback
"""

import os
import io
import base64
from PIL import Image
import pytesseract
from typing import Dict, Optional, Tuple

class OCRProcessor:
    def __init__(self):
        """Initialize OCR processor with safe Tesseract detection"""
        self.tesseract_available = False
        try:
            pytesseract.pytesseract.get_tesseract_version()
            self.tesseract_available = True
        except Exception:
            print("INFO: Tesseract OCR binary not detected on host system. Advanced image feature extraction mode active.")

    def is_ocr_available(self) -> bool:
        """Check if OCR text extraction is available"""
        return self.tesseract_available

    def encode_image_base64(self, image_path: str) -> Optional[str]:
        """Encode image file to base64 string for Vision LLM APIs"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image to base64: {e}")
            return None

    def extract_text_from_image(self, image_path: str, max_chars: int = 800) -> Dict:
        """Extract text from book cover or page image"""
        if not self.tesseract_available:
            return {
                'success': False,
                'extracted_text': '',
                'full_text': '',
                'source': 'Fallback (No OCR Binary)',
                'message': 'Tesseract OCR binary not detected on host environment.'
            }

        try:
            image = Image.open(image_path)
            max_size = (1600, 1600)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            extracted_text = pytesseract.image_to_string(image)
            cleaned_text = ' '.join(extracted_text.split())
            
            return {
                'success': True,
                'extracted_text': cleaned_text[:max_chars],
                'full_text': cleaned_text,
                'text_length': len(cleaned_text),
                'source': 'OCR'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'OCR extraction error: {str(e)}'
            }

    def analyze_book_cover(self, image_path: str) -> Dict:
        """
        Extract visual composition characteristics, palette, aspect ratio, and OCR text
        """
        try:
            image = Image.open(image_path)
            width, height = image.size
            
            cleaned_text = ""
            if self.tesseract_available:
                try:
                    text = pytesseract.image_to_string(image)
                    cleaned_text = ' '.join(text.split())
                except Exception:
                    pass

            image_rgb = image.convert('RGB')
            pixels = list(image_rgb.getdata())
            
            if pixels:
                sample_step = max(1, len(pixels) // 2000)
                sampled = pixels[::sample_step]
                r_avg = sum(p[0] for p in sampled) / len(sampled)
                g_avg = sum(p[1] for p in sampled) / len(sampled)
                b_avg = sum(p[2] for p in sampled) / len(sampled)
                
                if r_avg > 130 and g_avg < 100 and b_avg < 100:
                    dominant_color = 'Warm Crimson Red'
                elif b_avg > 130 and r_avg < 110:
                    dominant_color = 'Deep Sapphire Blue'
                elif g_avg > 120 and r_avg < 110:
                    dominant_color = 'Emerald Forest Green'
                elif r_avg > 180 and g_avg > 180 and b_avg > 180:
                    dominant_color = 'Bright Light / Minimalist White'
                elif r_avg < 70 and g_avg < 70 and b_avg < 70:
                    dominant_color = 'Dark Gothic / Noir Shadow'
                elif r_avg > 140 and g_avg > 100 and b_avg < 90:
                    dominant_color = 'Golden Amber Vintage'
                else:
                    dominant_color = 'Balanced Multi-tone'
            else:
                dominant_color = 'Unknown'

            aspect_ratio = round(width / height, 2) if height > 0 else 0.7
            orientation = "Portrait (Standard Book Cover)" if height > width else "Landscape / Wide Layout"
            
            # Simple title / author candidate parser
            lines = [l.strip() for l in cleaned_text.split('\n') if len(l.strip()) > 2]
            title_candidate = lines[0] if lines else ""
            author_candidate = lines[1] if len(lines) > 1 else ""

            return {
                'success': True,
                'image_size': f'{width}x{height} px',
                'orientation': orientation,
                'aspect_ratio': aspect_ratio,
                'extracted_text': cleaned_text[:400] if cleaned_text else '',
                'title_candidate': title_candidate,
                'author_candidate': author_candidate,
                'dominant_color': dominant_color,
                'has_text': len(cleaned_text) > 15,
                'ocr_available': self.tesseract_available
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Cover analysis error: {str(e)}'
            }

    def get_book_info_from_image(self, image_path: str) -> Dict:
        """
        Get complete book info extracted from image
        """
        return self.analyze_book_cover(image_path)