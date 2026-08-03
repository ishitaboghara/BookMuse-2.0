"""
BookMuse 2.0 - Genre System
Flashcards, recommendations, and genre-based features
"""

from typing import List, Dict, Optional
from config import GENRES

class GenreSystem:
    def __init__(self, books_db):
        """
        Initialize genre system
        
        Args:
            books_db: BookHandler instance with all books
        """
        self.books_db = books_db
        self.flashcards = self._generate_flashcards()
    
    # ============================================================================
    # FLASHCARD GENERATION
    # ============================================================================
    
    def _generate_flashcards(self) -> Dict[str, List[Dict]]:
        """
        Generate flashcards for each genre
        
        Returns:
            Dictionary of flashcards by genre
        """
        flashcards = {}
        
        for genre in GENRES:
            genre_books = self.books_db.get_books_by_genre(genre)
            flashcards[genre] = self._create_genre_flashcards(genre_books, genre)
        
        return flashcards
    
    def _create_genre_flashcards(self, books: List[Dict], genre: str) -> List[Dict]:
        """
        Create flashcards from books in a genre
        
        Args:
            books: List of books in genre
            genre: Genre name
        
        Returns:
            List of flashcard dictionaries
        """
        cards = []
        
        for book in books:
            # Card 1: Book Title & Author
            cards.append({
                'id': f"{book['id']}_1",
                'genre': genre,
                'book_id': book['id'],
                'type': 'title_author',
                'front': f"📚 What book is this?",
                'back': f"{book['title']} by {book['author']}",
                'difficulty': 'easy',
                'year': book.get('year', 'Unknown')
            })
            
            # Card 2: Plot Summary
            cards.append({
                'id': f"{book['id']}_2",
                'genre': genre,
                'book_id': book['id'],
                'type': 'plot',
                'front': f"📖 What is '{book['title']}' about?",
                'back': book.get('summary', 'No summary available'),
                'difficulty': 'medium',
                'book_title': book['title']
            })
            
            # Card 3: Themes
            if book.get('key_themes'):
                themes_str = ', '.join(book['key_themes'])
                cards.append({
                    'id': f"{book['id']}_3",
                    'genre': genre,
                    'book_id': book['id'],
                    'type': 'themes',
                    'front': f"🎭 What are the main themes in '{book['title']}'?",
                    'back': themes_str,
                    'difficulty': 'medium',
                    'book_title': book['title']
                })
            
            # Card 4: Author Info
            cards.append({
                'id': f"{book['id']}_4",
                'genre': genre,
                'book_id': book['id'],
                'type': 'author',
                'front': f"✍️ Who wrote '{book['title']}'?",
                'back': f"{book['author']}",
                'difficulty': 'easy',
                'book_title': book['title']
            })
            
            # Card 5: Publication Year
            cards.append({
                'id': f"{book['id']}_5",
                'genre': genre,
                'book_id': book['id'],
                'type': 'year',
                'front': f"📅 When was '{book['title']}' published?",
                'back': f"{book.get('year', 'Unknown')}",
                'difficulty': 'easy',
                'book_title': book['title']
            })
            
            # Card 6: Rating
            cards.append({
                'id': f"{book['id']}_6",
                'genre': genre,
                'book_id': book['id'],
                'type': 'rating',
                'front': f"⭐ What is the rating of '{book['title']}'?",
                'back': f"{book.get('rating', 'N/A')}/5.0 stars",
                'difficulty': 'easy',
                'book_title': book['title']
            })
            
            # Card 7: Movie Adaptation
            if book.get('movie'):
                cards.append({
                    'id': f"{book['id']}_7",
                    'genre': genre,
                    'book_id': book['id'],
                    'type': 'movie',
                    'front': f"🎬 Was '{book['title']}' adapted into a movie?",
                    'back': f"Yes! '{book['movie']}' ({book.get('movie_year', 'N/A')})",
                    'difficulty': 'easy',
                    'book_title': book['title']
                })
            
            # Card 8: Character Knowledge
            cards.append({
                'id': f"{book['id']}_8",
                'genre': genre,
                'book_id': book['id'],
                'type': 'characters',
                'front': f"👥 Name a main character from '{book['title']}'",
                'back': "Check the book or ask BookMuse for character details!",
                'difficulty': 'hard',
                'book_title': book['title']
            })
        
        return cards
    
    # ============================================================================
    # GET FLASHCARDS BY GENRE
    # ============================================================================
    
    def get_genre_flashcards(self, genre: str) -> List[Dict]:
        """
        Get all flashcards for a specific genre
        
        Args:
            genre: Genre name
        
        Returns:
            List of flashcards for that genre
        """
        return self.flashcards.get(genre, [])
    
    def get_flashcards_by_difficulty(self, genre: str, difficulty: str) -> List[Dict]:
        """
        Get flashcards filtered by difficulty level
        
        Args:
            genre: Genre name
            difficulty: 'easy', 'medium', or 'hard'
        
        Returns:
            Filtered flashcard list
        """
        genre_cards = self.get_genre_flashcards(genre)
        return [c for c in genre_cards if c.get('difficulty') == difficulty]
    
    def get_random_flashcard(self, genre: str) -> Optional[Dict]:
        """
        Get a random flashcard from a genre
        
        Args:
            genre: Genre name
        
        Returns:
            Random flashcard
        """
        import random
        cards = self.get_genre_flashcards(genre)
        return random.choice(cards) if cards else None
    
    # ============================================================================
    # RECOMMENDATIONS
    # ============================================================================
    
    def get_genre_recommendations(self, genre: str, limit: int = 5) -> List[Dict]:
        """
        Get book recommendations for a genre
        
        Args:
            genre: Genre name
            limit: Number of recommendations
        
        Returns:
            List of recommended books
        """
        recommendations = self.books_db.get_recommendations(genre)
        return recommendations[:limit]
    
    def get_similar_books(self, book_id: int, limit: int = 5) -> List[Dict]:
        """
        Get books similar to a given book
        
        Args:
            book_id: ID of reference book
            limit: Number of similar books
        
        Returns:
            List of similar books
        """
        # Get the reference book
        books = self.books_db.get_all_books()
        ref_book = next((b for b in books if b['id'] == book_id), None)
        
        if not ref_book:
            return []
        
        genre = ref_book.get('genre', '')
        
        # Get recommendations from same genre, excluding the reference book
        similar = [
            b for b in self.books_db.get_recommendations(genre)
            if b['id'] != book_id
        ]
        
        return similar[:limit]
    
    def get_cross_genre_recommendations(self, liked_book_id: int, limit: int = 5) -> List[Dict]:
        """
        Get recommendations from other genres based on themes
        
        Args:
            liked_book_id: Book ID the user liked
            limit: Number of recommendations
        
        Returns:
            Cross-genre recommendations
        """
        books = self.books_db.get_all_books()
        liked_book = next((b for b in books if b['id'] == liked_book_id), None)
        
        if not liked_book:
            return []
        
        liked_themes = set(liked_book.get('key_themes', []))
        
        # Find books with similar themes in other genres
        recommendations = []
        for book in books:
            if book['id'] != liked_book_id:
                book_themes = set(book.get('key_themes', []))
                common_themes = liked_themes & book_themes
                
                if common_themes:
                    recommendations.append({
                        'book': book,
                        'common_themes': list(common_themes),
                        'match_score': len(common_themes) / max(len(liked_themes), len(book_themes))
                    })
        
        # Sort by match score and return top recommendations
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return [r['book'] for r in recommendations[:limit]]
    
    # ============================================================================
    # GENRE INFO & STATS
    # ============================================================================
    
    def get_genre_stats(self, genre: str) -> Dict:
        """
        Get statistics about a genre
        
        Args:
            genre: Genre name
        
        Returns:
            Dictionary with genre statistics
        """
        books = self.books_db.get_books_by_genre(genre)
        
        if not books:
            return {'error': f'No books found for genre: {genre}'}
        
        ratings = [b.get('rating', 0) for b in books if b.get('rating')]
        years = [b.get('year', 0) for b in books if b.get('year')]
        pages = [b.get('pages', 0) for b in books if b.get('pages')]
        
        return {
            'genre': genre,
            'book_count': len(books),
            'average_rating': round(sum(ratings) / len(ratings), 2) if ratings else 'N/A',
            'highest_rated': max(books, key=lambda x: x.get('rating', 0)) if books else None,
            'oldest_book': min(years) if years else 'N/A',
            'newest_book': max(years) if years else 'N/A',
            'average_pages': round(sum(pages) / len(pages), 0) if pages else 'N/A',
            'books_with_movies': len([b for b in books if b.get('movie')]),
            'flashcard_count': len(self.get_genre_flashcards(genre))
        }
    
    def get_all_genres_overview(self) -> Dict[str, Dict]:
        """
        Get overview of all genres
        
        Returns:
            Dictionary with stats for all genres
        """
        overview = {}
        for genre in GENRES:
            overview[genre] = self.get_genre_stats(genre)
        return overview
    
    # ============================================================================
    # GENRE-BASED LEARNING PATHS
    # ============================================================================
    
    def create_learning_path(self, genre: str, duration_minutes: int = 60) -> Dict:
        """
        Create a learning path for a genre
        
        Args:
            genre: Genre name
            duration_minutes: Estimated time available
        
        Returns:
            Structured learning path
        """
        stats = self.get_genre_stats(genre)
        cards = self.get_genre_flashcards(genre)
        books = self.books_db.get_books_by_genre(genre)
        
        # Estimate: 2 mins per easy card, 4 mins per medium, 6 mins per hard
        easy_cards = [c for c in cards if c.get('difficulty') == 'easy']
        medium_cards = [c for c in cards if c.get('difficulty') == 'medium']
        hard_cards = [c for c in cards if c.get('difficulty') == 'hard']
        
        return {
            'genre': genre,
            'duration_minutes': duration_minutes,
            'structure': {
                'phase_1_basics': {
                    'duration': 15,
                    'cards': easy_cards[:10],
                    'goal': 'Learn basic book titles and authors'
                },
                'phase_2_understanding': {
                    'duration': 25,
                    'cards': medium_cards[:10],
                    'goal': 'Understand plots and themes'
                },
                'phase_3_mastery': {
                    'duration': 20,
                    'cards': hard_cards[:10],
                    'goal': 'Master detailed knowledge'
                }
            },
            'recommended_reading': books[:3],
            'total_flashcards': len(cards),
            'next_step': f"Start with Phase 1 to learn about {genre} books!"
        }
    
    # ============================================================================
    # POPULAR BOOKS BY GENRE
    # ============================================================================
    
    def get_top_rated_by_genre(self, genre: str, limit: int = 5) -> List[Dict]:
        """
        Get top-rated books in a genre
        
        Args:
            genre: Genre name
            limit: Number of books to return
        
        Returns:
            Top-rated books
        """
        books = self.books_db.get_books_by_genre(genre)
        sorted_books = sorted(books, key=lambda x: x.get('rating', 0), reverse=True)
        return sorted_books[:limit]
    
    def get_newest_by_genre(self, genre: str, limit: int = 5) -> List[Dict]:
        """
        Get newest books in a genre
        
        Args:
            genre: Genre name
            limit: Number of books to return
        
        Returns:
            Newest books
        """
        books = self.books_db.get_books_by_genre(genre)
        sorted_books = sorted(books, key=lambda x: x.get('year', 0), reverse=True)
        return sorted_books[:limit]