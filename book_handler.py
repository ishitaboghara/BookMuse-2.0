"""
BookMuse 2.0 - Book Handler System
Manages unlimited books, genres, recommendations, and metadata
"""

import json
import os
from typing import List, Dict, Optional
from config import GENRES

class BookHandler:
    def __init__(self):
        """Initialize book handler"""
        self.db_path = "data/books_database.json"
        self.books = self._load_database()
    
    def _load_database(self) -> List[Dict]:
        """Load books from JSON database"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._get_default_books()
        else:
            # Create database directory
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            books = self._get_default_books()
            self._save_database(books)
            return books
    
    def _save_database(self, books: List[Dict]):
        """Save books to JSON database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
    
    def _get_default_books(self) -> List[Dict]:
        """Get default book database (30+ books across genres)"""
        return [
            # Mystery
            {
                "id": 1,
                "title": "The Girl with the Dragon Tattoo",
                "author": "Stieg Larsson",
                "genre": "Mystery",
                "summary": "A gripping mystery about a journalist and a hacker investigating a decades-old disappearance.",
                "rating": 4.1,
                "pages": 465,
                "year": 2005,
                "movie": "The Girl with the Dragon Tattoo (2011)",
                "movie_director": "David Fincher",
                "movie_year": 2011,
                "book_vs_movie": "Book is more detailed and dark. Movie is faster-paced but loses some complexity.",
                "key_themes": ["mystery", "corruption", "journalism", "technology"],
                "reviews": [
                    "Incredibly gripping mystery with complex characters.",
                    "Dense but rewarding. Book is better than movie."
                ]
            },
            {
                "id": 2,
                "title": "Murder on the Orient Express",
                "author": "Agatha Christie",
                "genre": "Mystery",
                "summary": "Detective Hercule Poirot investigates a murder on a luxury train.",
                "rating": 4.3,
                "pages": 256,
                "year": 1934,
                "movie": "Murder on the Orient Express (2017)",
                "movie_director": "Kenneth Branagh",
                "movie_year": 2017,
                "book_vs_movie": "Book has better character development. Movie is more visually stunning.",
                "key_themes": ["mystery", "justice", "revenge", "morality"],
                "reviews": [
                    "Classic mystery with an ingenious plot twist.",
                    "Agatha Christie at her best."
                ]
            },
            
            # Romance
            {
                "id": 3,
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "genre": "Romance",
                "summary": "Elizabeth Bennet and Mr. Darcy navigate social expectations and find love.",
                "rating": 4.6,
                "pages": 279,
                "year": 1813,
                "movie": "Pride and Prejudice (2005)",
                "movie_director": "Joe Wright",
                "movie_year": 2005,
                "book_vs_movie": "Book has more wit and social commentary. Movie is romantically beautiful.",
                "key_themes": ["love", "social class", "independence", "prejudice"],
                "reviews": [
                    "Timeless romance with brilliant social satire.",
                    "Elizabeth Bennet is one of literature's greatest heroines."
                ]
            },
            {
                "id": 4,
                "title": "The Notebook",
                "author": "Nicholas Sparks",
                "genre": "Romance",
                "summary": "A heartwarming story of enduring love across decades.",
                "rating": 4.1,
                "pages": 214,
                "year": 1996,
                "movie": "The Notebook (2004)",
                "movie_director": "Nick Cassavetes",
                "movie_year": 2004,
                "book_vs_movie": "Book is more emotional. Movie captures the romance beautifully.",
                "key_themes": ["love", "memory", "sacrifice", "destiny"],
                "reviews": [
                    "Deeply moving love story that stays with you.",
                    "Perfect for romance lovers."
                ]
            },
            
            # Science Fiction
            {
                "id": 5,
                "title": "Dune",
                "author": "Frank Herbert",
                "genre": "Science Fiction",
                "summary": "Epic space opera about political intrigue, ecology, and power on a desert planet.",
                "rating": 4.3,
                "pages": 688,
                "year": 1965,
                "movie": "Dune (2021)",
                "movie_director": "Denis Villeneuve",
                "movie_year": 2021,
                "book_vs_movie": "Book is philosophically deeper. Movie is visually spectacular.",
                "key_themes": ["power", "ecology", "politics", "destiny"],
                "reviews": [
                    "Epic sci-fi masterpiece with incredible worldbuilding.",
                    "Complex and rewarding. Movie doesn't capture all nuances."
                ]
            },
            {
                "id": 6,
                "title": "1984",
                "author": "George Orwell",
                "genre": "Science Fiction",
                "summary": "Dystopian novel about totalitarianism and surveillance.",
                "rating": 4.2,
                "pages": 328,
                "year": 1949,
                "movie": "1984 (1984)",
                "movie_director": "Michael Radford",
                "movie_year": 1984,
                "book_vs_movie": "Book is more philosophical. Movie is more action-oriented.",
                "key_themes": ["totalitarianism", "surveillance", "freedom", "truth"],
                "reviews": [
                    "Haunting and prophetic.",
                    "Still terrifyingly relevant today."
                ]
            },
            
            # Fantasy
            {
                "id": 7,
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "genre": "Fantasy",
                "summary": "A reluctant hobbit goes on an epic adventure to reclaim treasure.",
                "rating": 4.3,
                "pages": 310,
                "year": 1937,
                "movie": "The Hobbit (2012-2014)",
                "movie_director": "Peter Jackson",
                "movie_year": 2012,
                "book_vs_movie": "Book is simpler and more adventurous. Movies are epic and action-packed.",
                "key_themes": ["adventure", "courage", "friendship", "journey"],
                "reviews": [
                    "Delightful fantasy adventure.",
                    "Perfect introduction to Middle-earth."
                ]
            },
            {
                "id": 8,
                "title": "Harry Potter and the Sorcerer's Stone",
                "author": "J.K. Rowling",
                "genre": "Fantasy",
                "summary": "A young wizard discovers his magical heritage and attends wizarding school.",
                "rating": 4.5,
                "pages": 309,
                "year": 1997,
                "movie": "Harry Potter and the Sorcerer's Stone (2001)",
                "movie_director": "Chris Columbus",
                "movie_year": 2001,
                "book_vs_movie": "Book has more world-building. Movie is a faithful adaptation.",
                "key_themes": ["magic", "friendship", "good vs evil", "belonging"],
                "reviews": [
                    "Magical and captivating.",
                    "Perfect for all ages."
                ]
            },
            
            # Thriller
            {
                "id": 9,
                "title": "The Da Vinci Code",
                "author": "Dan Brown",
                "genre": "Thriller",
                "summary": "Symbologist Robert Langdon races against time to solve a murder mystery.",
                "rating": 3.9,
                "pages": 454,
                "year": 2003,
                "movie": "The Da Vinci Code (2006)",
                "movie_director": "Ron Howard",
                "movie_year": 2006,
                "book_vs_movie": "Book is fast-paced. Movie is slower but visually beautiful.",
                "key_themes": ["mystery", "history", "religion", "secrets"],
                "reviews": [
                    "Page-turner with historical intrigue.",
                    "Controversial but captivating."
                ]
            },
            
            # Historical Fiction
            {
                "id": 10,
                "title": "The Book Thief",
                "author": "Markus Zusak",
                "genre": "Historical Fiction",
                "summary": "A girl steals books in Nazi Germany during WWII.",
                "rating": 4.4,
                "pages": 552,
                "year": 2005,
                "movie": "The Book Thief (2013)",
                "movie_director": "Brian Percival",
                "movie_year": 2013,
                "book_vs_movie": "Book is more poignant. Movie is beautiful but less impactful.",
                "key_themes": ["WWII", "books", "loss", "humanity"],
                "reviews": [
                    "Heartbreaking and beautiful.",
                    "Death as narrator is unique and powerful."
                ]
            },
            
            # Self-Help
            {
                "id": 11,
                "title": "Atomic Habits",
                "author": "James Clear",
                "genre": "Self-Help",
                "summary": "Practical guide to building better habits through tiny changes.",
                "rating": 4.4,
                "pages": 320,
                "year": 2018,
                "movie": None,
                "key_themes": ["habits", "productivity", "self-improvement", "systems"],
                "reviews": [
                    "Practical and actionable.",
                    "Changed how I think about habits."
                ]
            },
            
            # Memoir
            {
                "id": 12,
                "title": "Educated",
                "author": "Tara Westover",
                "genre": "Memoir",
                "summary": "A woman escapes her survivalist family to pursue education.",
                "rating": 4.3,
                "pages": 352,
                "year": 2018,
                "movie": None,
                "key_themes": ["education", "family", "survival", "freedom"],
                "reviews": [
                    "Powerful and inspiring.",
                    "Heartbreaking but ultimately hopeful."
                ]
            },
            
            # Comedy
            {
                "id": 13,
                "title": "Good Omens",
                "author": "Neil Gaiman & Terry Pratchett",
                "genre": "Comedy",
                "summary": "An angel and demon team up to prevent the apocalypse.",
                "rating": 4.3,
                "pages": 432,
                "year": 1990,
                "movie": "Good Omens (2019)",
                "movie_director": "Neil Gaiman",
                "movie_year": 2019,
                "book_vs_movie": "Book is hilarious. TV series captures the humor perfectly.",
                "key_themes": ["humor", "friendship", "good vs evil", "fate"],
                "reviews": [
                    "Hilarious and clever.",
                    "Perfect blend of humor and heart."
                ]
            },
            
            # Drama
            {
                "id": 14,
                "title": "The Kite Runner",
                "author": "Khaled Hosseini",
                "genre": "Drama",
                "summary": "A story of friendship, betrayal, and redemption in Afghanistan.",
                "rating": 4.3,
                "pages": 324,
                "year": 2003,
                "movie": "The Kite Runner (2007)",
                "movie_director": "Marc Forster",
                "movie_year": 2007,
                "book_vs_movie": "Book is more introspective. Movie captures the emotion well.",
                "key_themes": ["friendship", "betrayal", "redemption", "Afghanistan"],
                "reviews": [
                    "Deeply moving and emotional.",
                    "Explores complex moral issues."
                ]
            },
            
            # Horror
            {
                "id": 15,
                "title": "The Shining",
                "author": "Stephen King",
                "genre": "Horror",
                "summary": "A family isolated in a haunted hotel during winter descends into madness.",
                "rating": 4.2,
                "pages": 447,
                "year": 1977,
                "movie": "The Shining (1980)",
                "movie_director": "Stanley Kubrick",
                "movie_year": 1980,
                "book_vs_movie": "Book is more psychological. Movie is visually terrifying.",
                "key_themes": ["horror", "isolation", "madness", "family"],
                "reviews": [
                    "Terrifying and psychological.",
                    "One of Stephen King's best."
                ]
            },
            
            # Adventure
            {
                "id": 16,
                "title": "The Count of Monte Cristo",
                "author": "Alexandre Dumas",
                "genre": "Adventure",
                "summary": "A man wrongly imprisoned escapes and seeks elaborate revenge.",
                "rating": 4.3,
                "pages": 462,
                "year": 1844,
                "movie": "The Count of Monte Cristo (2002)",
                "movie_director": "Kevin Reynolds",
                "movie_year": 2002,
                "book_vs_movie": "Book is epic and detailed. Movie is action-packed.",
                "key_themes": ["revenge", "adventure", "justice", "redemption"],
                "reviews": [
                    "Epic adventure and revenge.",
                    "Timeless classic."
                ]
            },
        ]
    
    def get_all_books(self) -> List[Dict]:
        """Get all books"""
        return self.books
    
    def get_books_by_genre(self, genre: str) -> List[Dict]:
        """Get books by genre"""
        return [b for b in self.books if b.get('genre', '').lower() == genre.lower()]
    
    def get_book_by_title(self, title: str) -> Optional[Dict]:
        """Get book by title"""
        for book in self.books:
            if book['title'].lower() == title.lower():
                return book
        return None
    
    def search_books(self, query: str) -> List[Dict]:
        """Search books by title, author, or genre"""
        query = query.lower()
        results = []
        for book in self.books:
            if (query in book['title'].lower() or 
                query in book['author'].lower() or
                query in book.get('genre', '').lower()):
                results.append(book)
        return results
    
    def get_recommendations(self, genre: str, exclude_book_id: Optional[int] = None) -> List[Dict]:
        """Get book recommendations by genre"""
        books = self.get_books_by_genre(genre)
        if exclude_book_id:
            books = [b for b in books if b['id'] != exclude_book_id]
        return sorted(books, key=lambda x: x.get('rating', 0), reverse=True)[:5]
    
    def add_book(self, book: Dict) -> bool:
        """Add new book to database"""
        if not self.get_book_by_title(book.get('title', '')):
            book['id'] = max([b['id'] for b in self.books], default=0) + 1
            self.books.append(book)
            self._save_database(self.books)
            return True
        return False
    
    def get_movie_info(self, book_id: int) -> Optional[Dict]:
        """Get movie adaptation information"""
        book = next((b for b in self.books if b['id'] == book_id), None)
        if book:
            return {
                'has_movie': bool(book.get('movie')),
                'movie_title': book.get('movie'),
                'movie_year': book.get('movie_year'),
                'movie_director': book.get('movie_director'),
                'book_vs_movie': book.get('book_vs_movie')
            }
        return None