"""
BookMuse 2.0 - Movie Comparison
Compare books with their movie adaptations
"""

from typing import Dict, List, Optional

class MovieComparison:
    def __init__(self, books_db):
        """
        Initialize movie comparison system
        
        Args:
            books_db: BookHandler instance
        """
        self.books_db = books_db
    
    # ============================================================================
    # GET MOVIE ADAPTATION INFO
    # ============================================================================
    
    def get_movie_adaptation(self, book_id: int) -> Dict:
        """
        Get movie adaptation info for a book
        
        Args:
            book_id: ID of the book
        
        Returns:
            Movie adaptation information
        """
        books = self.books_db.get_all_books()
        book = next((b for b in books if b['id'] == book_id), None)
        
        if not book:
            return {'error': 'Book not found'}
        
        if not book.get('movie'):
            return {
                'has_movie': False,
                'book_title': book['title'],
                'message': f"'{book['title']}' has not been adapted into a movie (yet!)"
            }
        
        return {
            'has_movie': True,
            'book_title': book['title'],
            'book_author': book['author'],
            'book_year': book.get('year'),
            'book_rating': book.get('rating'),
            'movie_title': book.get('movie'),
            'movie_director': book.get('movie_director'),
            'movie_year': book.get('movie_year'),
            'book_vs_movie': book.get('book_vs_movie', 'No comparison available'),
            'comparison_details': self._get_detailed_comparison(book)
        }
    
    def _get_detailed_comparison(self, book: Dict) -> Dict:
        """
        Get detailed comparison between book and movie
        
        Args:
            book: Book dictionary
        
        Returns:
            Detailed comparison
        """
        comparison = {
            'aspects': {
                'storytelling': self._compare_storytelling(book),
                'character_development': self._compare_characters(book),
                'pacing': self._compare_pacing(book),
                'visual_elements': self._compare_visuals(book),
                'emotional_impact': self._compare_emotion(book)
            },
            'book_advantages': self._book_advantages(book),
            'movie_advantages': self._movie_advantages(book),
            'recommendation': self._recommendation(book)
        }
        return comparison
    
    def _compare_storytelling(self, book: Dict) -> Dict:
        """Compare storytelling between book and movie"""
        return {
            'aspect': 'Storytelling',
            'book': 'More detailed narrative with internal monologues and subplots',
            'movie': 'Condensed story focused on main plot points',
            'winner': 'Book usually wins for complexity'
        }
    
    def _compare_characters(self, book: Dict) -> Dict:
        """Compare character development"""
        return {
            'aspect': 'Character Development',
            'book': 'Deeper exploration of motivations and emotions',
            'movie': 'Visual portrayal by actors, may lack depth',
            'winner': 'Book usually wins for depth'
        }
    
    def _compare_pacing(self, book: Dict) -> Dict:
        """Compare pacing"""
        return {
            'aspect': 'Pacing',
            'book': f"Can be slower, average {book.get('pages', 300)} pages to read",
            'movie': 'Faster-paced, ~2-3 hours runtime',
            'winner': 'Movie for quick consumption, Book for immersion'
        }
    
    def _compare_visuals(self, book: Dict) -> Dict:
        """Compare visual elements"""
        return {
            'aspect': 'Visual Elements',
            'book': 'Uses imagination - each reader visualizes differently',
            'movie': 'Professional cinematography, sets, costumes',
            'winner': 'Movie for visual spectacle'
        }
    
    def _compare_emotion(self, book: Dict) -> Dict:
        """Compare emotional impact"""
        return {
            'aspect': 'Emotional Impact',
            'book': 'Builds slowly through detailed narrative',
            'movie': 'Relies on actor performances and music',
            'winner': 'Depends on personal preference'
        }
    
    def _book_advantages(self, book: Dict) -> List[str]:
        """List advantages of the book"""
        advantages = [
            '📖 More detailed and comprehensive storytelling',
            '💭 Access to characters\' inner thoughts and emotions',
            '🎨 Freedom to imagine scenes and characters yourself',
            '⏰ Can go deeper into subplots and side stories',
            '📚 Original author\'s complete vision',
            '🧠 Engages imagination and critical thinking',
            '💰 Usually less expensive than watching movies'
        ]
        return advantages
    
    def _movie_advantages(self, book: Dict) -> List[str]:
        """List advantages of the movie"""
        advantages = [
            '🎬 Professional cinematography and visual effects',
            '⏱️ Can watch in 2-3 hours vs days of reading',
            '🎭 Talented actors bring characters to life',
            '🎵 Musical scores enhance emotional moments',
            '🎨 Professional production design and costumes',
            '📱 Easy to watch on various devices',
            '👥 Great for group viewing experiences'
        ]
        return advantages
    
    def _recommendation(self, book: Dict) -> Dict:
        """Get viewing recommendation"""
        return {
            'read_first_or_watch_first': 'Usually read the book first',
            'reasoning': [
                'Book provides deeper context and understanding',
                'Avoids spoilers if you watch movie first',
                'Appreciate cinematography more after reading',
                'Make your own character interpretations'
            ],
            'suggestion': f"Read '{book['title']}' then watch '{book.get('movie', 'the adaptation')}' and compare!"
        }
    
    # ============================================================================
    # GET ALL BOOKS WITH MOVIES
    # ============================================================================
    
    def get_all_books_with_movies(self) -> List[Dict]:
        """
        Get all books that have movie adaptations
        
        Returns:
            List of books with movies
        """
        books = self.books_db.get_all_books()
        return [b for b in books if b.get('movie')]
    
    def get_books_by_director(self, director: str) -> List[Dict]:
        """
        Get books adapted by a specific director
        
        Args:
            director: Director name
        
        Returns:
            List of books by that director
        """
        books = self.books_db.get_all_books()
        return [b for b in books if b.get('movie_director', '').lower() == director.lower()]
    
    def get_books_with_movies_by_genre(self, genre: str) -> List[Dict]:
        """
        Get books with movies in a specific genre
        
        Args:
            genre: Genre name
        
        Returns:
            List of books with movies
        """
        books = self.books_db.get_books_by_genre(genre)
        return [b for b in books if b.get('movie')]
    
    # ============================================================================
    # MOVIE STATISTICS
    # ============================================================================
    
    def get_movie_statistics(self) -> Dict:
        """
        Get statistics about book-to-movie adaptations
        
        Returns:
            Movie adaptation statistics
        """
        books = self.books_db.get_all_books()
        books_with_movies = [b for b in books if b.get('movie')]
        
        if not books_with_movies:
            return {'total_books': len(books), 'books_with_movies': 0}
        
        movie_years = [b.get('movie_year') for b in books_with_movies if b.get('movie_year')]
        book_years = [b.get('year') for b in books_with_movies if b.get('year')]
        
        # Calculate adaptation lag (years between book and movie)
        lags = []
        for i, year in enumerate(movie_years):
            if i < len(book_years):
                lag = year - book_years[i]
                if lag > 0:
                    lags.append(lag)
        
        return {
            'total_books_in_database': len(books),
            'books_with_movies': len(books_with_movies),
            'percentage_adapted': f"{(len(books_with_movies)/len(books)*100):.1f}%",
            'earliest_adaptation': min(movie_years) if movie_years else 'N/A',
            'latest_adaptation': max(movie_years) if movie_years else 'N/A',
            'average_adaptation_lag': f"{sum(lags)/len(lags):.0f} years" if lags else 'N/A',
            'directors': list(set([b.get('movie_director') for b in books_with_movies if b.get('movie_director')]))
        }
    
    # ============================================================================
    # DISCUSSION PROMPTS
    # ============================================================================
    
    def get_discussion_prompts(self, book_id: int) -> Dict:
        """
        Get discussion prompts for book vs movie
        
        Args:
            book_id: Book ID
        
        Returns:
            Discussion prompts
        """
        books = self.books_db.get_all_books()
        book = next((b for b in books if b['id'] == book_id), None)
        
        if not book or not book.get('movie'):
            return {'error': 'No movie adaptation found'}
        
        prompts = {
            'book_title': book['title'],
            'movie_title': book.get('movie'),
            'discussion_questions': [
                {
                    'question': 'Which version did you enjoy more - the book or the movie?',
                    'why': 'Helps identify personal preferences for storytelling'
                },
                {
                    'question': f"What important plot points from the book were left out of the movie?",
                    'why': 'Explores adaptation choices and their impact'
                },
                {
                    'question': "How did the movie\'s portrayal of characters compare to how you imagined them from the book?",
                    'why': 'Compares imagination vs visual representation'
                },
                {
                    'question': "Did the movie capture the emotional tone of the book?",
                    'why': 'Explores emotional authenticity in adaptations'
                },
                {
                    'question': f"If you were directing this movie, what would you have done differently?",
                    'why': 'Encourages creative thinking about adaptation'
                },
                {
                    'question': "Do you think the movie helps people understand the book better?",
                    'why': 'Examines the relationship between mediums'
                }
            ],
            'reflection_prompts': [
                'The book helped me appreciate the complexity of...',
                'The movie made me realize...',
                'If I could change one thing about the adaptation, it would be...',
                'The book and movie are similar because...',
                'The most significant difference is...'
            ]
        }
        
        return prompts
    
    # ============================================================================
    # CREATE COMPARISON REPORT
    # ============================================================================
    
    def create_comparison_report(self, book_id: int) -> Dict:
        """
        Create a comprehensive comparison report
        
        Args:
            book_id: Book ID
        
        Returns:
            Full comparison report
        """
        books = self.books_db.get_all_books()
        book = next((b for b in books if b['id'] == book_id), None)
        
        if not book:
            return {'error': 'Book not found'}
        
        if not book.get('movie'):
            return {
                'book_title': book['title'],
                'has_movie': False,
                'message': 'This book does not have a movie adaptation'
            }
        
        report = {
            'title': f"Book vs Movie: {book['title']}",
            'book_info': {
                'title': book['title'],
                'author': book['author'],
                'published': book.get('year'),
                'pages': book.get('pages'),
                'rating': book.get('rating'),
                'genre': book.get('genre'),
                'themes': book.get('key_themes', [])
            },
            'movie_info': {
                'title': book.get('movie'),
                'director': book.get('movie_director'),
                'released': book.get('movie_year'),
                'adaptation_lag': f"{book.get('movie_year', 0) - book.get('year', 0)} years after publication"
            },
            'comparison': self._get_detailed_comparison(book),
            'discussion_points': self.get_discussion_prompts(book_id),
            'recommendation': {
                'should_read_book': True,
                'should_watch_movie': True,
                'read_first': True,
                'both_offer': 'Different but complementary experiences'
            },
            'summary': book.get('book_vs_movie', 'Compare both versions to appreciate each medium!')
        }
        
        return report
    
    # ============================================================================
    # FIND SIMILAR ADAPTATIONS
    # ============================================================================
    
    def find_similar_adaptations(self, book_id: int, limit: int = 5) -> List[Dict]:
        """
        Find books with similar adaptations
        
        Args:
            book_id: Reference book ID
            limit: Number of similar adaptations
        
        Returns:
            List of similar book-movie adaptations
        """
        books = self.books_db.get_all_books()
        ref_book = next((b for b in books if b['id'] == book_id), None)
        
        if not ref_book or not ref_book.get('movie'):
            return []
        
        ref_genre = ref_book.get('genre', '')
        ref_director = ref_book.get('movie_director', '')
        ref_year = ref_book.get('year', 0)
        
        similar = []
        for book in books:
            if book['id'] != book_id and book.get('movie'):
                # Score based on similarity
                score = 0
                if book.get('genre') == ref_genre:
                    score += 30
                if book.get('movie_director') == ref_director:
                    score += 40
                if abs(book.get('year', 0) - ref_year) < 20:
                    score += 20
                
                if score > 0:
                    similar.append({
                        'book': book,
                        'similarity_score': score
                    })
        
        # Sort by score and return top matches
        similar.sort(key=lambda x: x['similarity_score'], reverse=True)
        return [s['book'] for s in similar[:limit]]