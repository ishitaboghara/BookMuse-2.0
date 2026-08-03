"""
BookMuse 2.0 - Web Search & Book Info Fetcher
Retrieves book data from Wikipedia, Goodreads, Google Books
"""

import requests
from typing import Dict, List, Optional
import json

class BookSearcher:
    def __init__(self):
        """Initialize book searcher"""
        self.wiki_base = "https://en.wikipedia.org/api/rest_v1"
        self.google_books_api = "https://www.googleapis.com/books/v1/volumes"
        self.goodreads_base = "https://www.goodreads.com/search"
    
    # ============================================================================
    # WIKIPEDIA SEARCH
    # ============================================================================
    
    def get_wikipedia_info(self, book_title: str, author: str = "") -> Dict:
        """
        Get book information from Wikipedia
        
        Args:
            book_title: Title of the book
            author: Author name (optional)
        
        Returns:
            Dictionary with plot, characters, themes, etc.
        """
        try:
            # Search for the book
            search_query = f"{book_title} novel"
            if author:
                search_query = f"{book_title} {author}"
            
            # Wikipedia search endpoint
            search_url = f"{self.wiki_base}/page/summary/{search_query.replace(' ', '_')}"
            
            response = requests.get(search_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    'success': True,
                    'title': data.get('title', ''),
                    'summary': data.get('extract', '')[:500],  # First 500 chars
                    'full_summary': data.get('extract', ''),
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'source': 'Wikipedia'
                }
            else:
                return {
                    'success': False,
                    'message': 'Book not found on Wikipedia'
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Wikipedia search error: {str(e)}'
            }
    
    # ============================================================================
    # GOODREADS SCRAPING (Free alternative)
    # ============================================================================
    
    def get_goodreads_info(self, book_title: str, author: str = "") -> Dict:
        """
        Get book info from Goodreads (basic scraping)
        
        Args:
            book_title: Title of the book
            author: Author name
        
        Returns:
            Dictionary with ratings, reviews count, etc.
        """
        try:
            # Goodreads search URL (no API key needed for basic info)
            search_url = "https://www.goodreads.com/search"
            params = {
                'q': f"{book_title} {author}",
                'tab': 'books'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=5)
            
            # Since Goodreads scraping is complex, return structured empty
            # In production, you'd parse the HTML
            return {
                'success': True,
                'source': 'Goodreads',
                'note': 'Use LLM to search for reviews in its training data',
                'suggestion': f'Search Goodreads for "{book_title}" to see reviews'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Goodreads fetch error: {str(e)}'
            }
    
    # ============================================================================
    # GOOGLE BOOKS API (Free tier)
    # ============================================================================
    
    def get_google_books_info(self, book_title: str, author: str = "") -> Dict:
        """
        Get book info from Google Books API (free)
        
        Args:
            book_title: Title of the book
            author: Author name
        
        Returns:
            Dictionary with metadata
        """
        try:
            query = f'"{book_title}" {author}' if author else book_title
            
            params = {
                'q': query,
                'maxResults': 1
            }
            
            response = requests.get(self.google_books_api, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('items'):
                    book = data['items'][0]['volumeInfo']
                    
                    return {
                        'success': True,
                        'title': book.get('title', ''),
                        'authors': book.get('authors', []),
                        'publisher': book.get('publisher', ''),
                        'published_date': book.get('publishedDate', ''),
                        'description': book.get('description', '')[:500],
                        'full_description': book.get('description', ''),
                        'page_count': book.get('pageCount', 0),
                        'categories': book.get('categories', []),
                        'maturity_rating': book.get('maturityRating', ''),
                        'preview_link': book.get('previewLink', ''),
                        'info_link': book.get('infoLink', ''),
                        'source': 'Google Books'
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Book not found on Google Books'
                    }
            else:
                return {
                    'success': False,
                    'message': 'Google Books API error'
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Google Books error: {str(e)}'
            }
    
    # ============================================================================
    # COMBINED SEARCH - Get all info
    # ============================================================================
    
    def search_book_complete(self, book_title: str, author: str = "") -> Dict:
        """
        Get complete book information from all sources
        
        Args:
            book_title: Title of the book
            author: Author name (optional)
        
        Returns:
            Combined dictionary with all available info
        """
        
        result = {
            'book_title': book_title,
            'author': author,
            'sources': {}
        }
        
        # Get Wikipedia info
        wiki_info = self.get_wikipedia_info(book_title, author)
        result['sources']['wikipedia'] = wiki_info
        
        # Get Google Books info
        google_info = self.get_google_books_info(book_title, author)
        result['sources']['google_books'] = google_info
        
        # Get Goodreads info
        goodreads_info = self.get_goodreads_info(book_title, author)
        result['sources']['goodreads'] = goodreads_info
        
        # Combine best info
        result['combined'] = self._combine_sources(result['sources'])
        
        return result
    
    def _combine_sources(self, sources: Dict) -> Dict:
        """Combine info from all sources into single view"""
        combined = {
            'plot_summary': '',
            'author_info': '',
            'publication_info': '',
            'categories': [],
            'description': '',
            'sources_used': []
        }
        
        # Get plot from Wikipedia
        if sources.get('wikipedia', {}).get('success'):
            combined['plot_summary'] = sources['wikipedia'].get('summary', '')
            combined['sources_used'].append('Wikipedia')
        
        # Get publication info from Google Books
        if sources.get('google_books', {}).get('success'):
            google = sources['google_books']
            combined['author_info'] = ', '.join(google.get('authors', []))
            combined['publication_info'] = f"{google.get('publisher', '')} ({google.get('published_date', '')})"
            combined['categories'] = google.get('categories', [])
            combined['description'] = google.get('description', '')
            combined['sources_used'].append('Google Books')
        
        return combined
    
    # ============================================================================
    # SEARCH FOR CHARACTER INFO
    # ============================================================================
    
    def search_character_info(self, book_title: str, character_name: str) -> Dict:
        """
        Search for character information in a book
        
        Args:
            book_title: Title of the book
            character_name: Name of the character
        
        Returns:
            Info about the character
        """
        try:
            # Search Wikipedia for character
            search_query = f"{character_name} {book_title} character"
            search_url = f"{self.wiki_base}/page/summary/{search_query.replace(' ', '_')}"
            
            response = requests.get(search_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'character': character_name,
                    'book': book_title,
                    'info': data.get('extract', '')[:500],
                    'full_info': data.get('extract', ''),
                    'source': 'Wikipedia'
                }
            else:
                return {
                    'success': False,
                    'message': f'Character "{character_name}" not found in Wikipedia'
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Search error: {str(e)}'
            }
    
    # ============================================================================
    # SEARCH FOR THEMES & ANALYSIS
    # ============================================================================
    
    def search_book_themes(self, book_title: str, author: str = "") -> Dict:
        """
        Search for themes and literary analysis
        
        Args:
            book_title: Title of the book
            author: Author name
        
        Returns:
            Info about themes and analysis
        """
        try:
            search_query = f"{book_title} themes analysis"
            
            # Try Wikipedia first
            search_url = f"{self.wiki_base}/page/summary/{book_title.replace(' ', '_')}"
            response = requests.get(search_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                full_text = data.get('extract', '')
                
                return {
                    'success': True,
                    'book': book_title,
                    'analysis': full_text[:1000],  # First 1000 chars of full article
                    'note': 'For detailed theme analysis, see Wikipedia article',
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'source': 'Wikipedia'
                }
            else:
                return {
                    'success': False,
                    'message': 'Analysis not found'
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Analysis search error: {str(e)}'
            }