"""
BookMuse 2.0 - RAG Engine
Retrieval-Augmented Generation using FAISS and Sentence Transformers
"""

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Optional
from config import EMBEDDING_MODEL, EMBEDDING_DIM

class RAGEngine:
    def __init__(self, books_db):
        """
        Initialize RAG engine
        
        Args:
            books_db: BookHandler instance
        """
        self.books_db = books_db
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None
        self.passages = []
        self.book_passages = {}
        
        # Initialize with book data
        self._initialize_passages()
    
    # ============================================================================
    # INITIALIZE PASSAGES FROM BOOKS
    # ============================================================================
    
    def _initialize_passages(self):
        """Initialize passages from all books in database"""
        
        books = self.books_db.get_all_books()
        
        for book in books:
            book_id = book['id']
            passages = []
            
            # Add title
            passages.append(f"Title: {book['title']}")
            
            # Add author
            passages.append(f"Author: {book['author']}")
            
            # Add summary
            if book.get('summary'):
                passages.append(f"Summary: {book['summary']}")
            
            # Add genre
            if book.get('genre'):
                passages.append(f"Genre: {book['genre']}")
            
            # Add themes
            if book.get('key_themes'):
                themes = ', '.join(book['key_themes'])
                passages.append(f"Themes: {themes}")
            
            # Add year
            if book.get('year'):
                passages.append(f"Published: {book['year']}")
            
            # Add pages
            if book.get('pages'):
                passages.append(f"Pages: {book['pages']}")
            
            # Add rating
            if book.get('rating'):
                passages.append(f"Rating: {book['rating']}/5.0")
            
            # Add movie info
            if book.get('movie'):
                passages.append(f"Movie: {book['movie']} ({book.get('movie_year', 'N/A')})")
                if book.get('book_vs_movie'):
                    passages.append(f"Book vs Movie: {book['book_vs_movie']}")
            
            # Add reviews
            if book.get('reviews'):
                reviews_text = ' '.join(book['reviews'])
                passages.append(f"Reviews: {reviews_text}")
            
            self.book_passages[book_id] = passages
        
        self.passages = self._flatten_passages()
    
    def _flatten_passages(self) -> List[str]:
        """Flatten book passages into a single list"""
        all_passages = []
        for passages in self.book_passages.values():
            all_passages.extend(passages)
        return all_passages
    
    # ============================================================================
    # ADD CUSTOM PASSAGES
    # ============================================================================
    
    def add_passages(self, book_id: int, passages: List[str]):
        """
        Add custom passages for a book
        
        Args:
            book_id: Book ID
            passages: List of text passages
        """
        if book_id not in self.book_passages:
            self.book_passages[book_id] = []
        
        self.book_passages[book_id].extend(passages)
        self.passages = self._flatten_passages()
    
    def add_web_passages(self, book_title: str, passages: List[str]):
        """
        Add passages from web search (Wikipedia, etc.)
        
        Args:
            book_title: Title of the book
            passages: Passages from web
        """
        # Use negative ID for web passages
        web_id = -hash(book_title) % 1000000
        
        if web_id not in self.book_passages:
            self.book_passages[web_id] = []
        
        self.book_passages[web_id].extend(passages)
        self.passages = self._flatten_passages()
    
    # ============================================================================
    # RETRIEVE RELEVANT PASSAGES
    # ============================================================================
    
    def retrieve(self, query: str, k: int = 5) -> List[str]:
        """
        Retrieve relevant passages for a query
        
        Args:
            query: Search query
            k: Number of passages to retrieve
        
        Returns:
            List of relevant passages
        """
        try:
            if not self.passages:
                return []
            
            # Encode query
            query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)
            query_embedding = np.array([query_embedding]).astype('float32')
            
            # Encode all passages
            passage_embeddings = self.embedding_model.encode(
                self.passages, 
                convert_to_tensor=False
            )
            passage_embeddings = np.array(passage_embeddings).astype('float32')
            
            # Calculate similarity using cosine distance
            from sklearn.metrics.pairwise import cosine_distances
            distances = cosine_distances(query_embedding, passage_embeddings)[0]
            
            # Get top-k passages (lowest distance = highest similarity)
            top_k_indices = np.argsort(distances)[:min(k, len(self.passages))]
            
            retrieved_passages = [self.passages[i] for i in top_k_indices]
            
            return retrieved_passages
        
        except Exception as e:
            print(f"⚠️ RAG Retrieval Error: {str(e)}")
            return []
    
    def retrieve_by_book(self, query: str, book_id: int, k: int = 5) -> List[str]:
        """
        Retrieve passages specific to a book
        
        Args:
            query: Search query
            book_id: Book ID to search in
            k: Number of passages to retrieve
        
        Returns:
            Relevant passages from the book
        """
        try:
            if book_id not in self.book_passages:
                return []
            
            book_passages = self.book_passages[book_id]
            
            if not book_passages:
                return []
            
            # Encode query
            query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)
            query_embedding = np.array([query_embedding]).astype('float32')
            
            # Encode book passages
            passage_embeddings = self.embedding_model.encode(
                book_passages, 
                convert_to_tensor=False
            )
            passage_embeddings = np.array(passage_embeddings).astype('float32')
            
            # Calculate similarity
            from sklearn.metrics.pairwise import cosine_distances
            distances = cosine_distances(query_embedding, passage_embeddings)[0]
            
            # Get top-k from this book
            top_k_indices = np.argsort(distances)[:min(k, len(book_passages))]
            
            retrieved = [book_passages[i] for i in top_k_indices]
            
            return retrieved
        
        except Exception as e:
            print(f"⚠️ Book-specific retrieval error: {str(e)}")
            return []
    
    # ============================================================================
    # RETRIEVE WITH SCORES
    # ============================================================================
    
    def retrieve_with_scores(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve passages with similarity scores
        
        Args:
            query: Search query
            k: Number of passages to retrieve
        
        Returns:
            List of dicts with passages and scores
        """
        try:
            if not self.passages:
                return []
            
            # Encode query and passages
            query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)
            query_embedding = np.array([query_embedding]).astype('float32')
            
            passage_embeddings = self.embedding_model.encode(
                self.passages, 
                convert_to_tensor=False
            )
            passage_embeddings = np.array(passage_embeddings).astype('float32')
            
            # Calculate similarity (convert distance to similarity: 1 - distance)
            from sklearn.metrics.pairwise import cosine_distances
            distances = cosine_distances(query_embedding, passage_embeddings)[0]
            similarities = 1 - distances
            
            # Get top-k
            top_k_indices = np.argsort(similarities)[::-1][:min(k, len(self.passages))]
            
            results = [
                {
                    'passage': self.passages[i],
                    'similarity_score': float(similarities[i]),
                    'distance': float(distances[i])
                }
                for i in top_k_indices
            ]
            
            return results
        
        except Exception as e:
            print(f"⚠️ Scoring error: {str(e)}")
            return []
    
    # ============================================================================
    # SEMANTIC SEARCH
    # ============================================================================
    
    def semantic_search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Perform semantic search (same as retrieve_with_scores)
        
        Args:
            query: Search query
            k: Number of results
        
        Returns:
            List of relevant passages with scores
        """
        return self.retrieve_with_scores(query, k)
    
    # ============================================================================
    # BUILD CONTEXT FOR LLM
    # ============================================================================
    
    def build_context(self, query: str, book_id: int = None, k: int = 5) -> str:
        """
        Build context string for LLM prompt
        
        Args:
            query: Search query
            book_id: Specific book to search (optional)
            k: Number of passages
        
        Returns:
            Context string formatted for LLM
        """
        
        # Get relevant passages
        if book_id:
            passages = self.retrieve_by_book(query, book_id, k)
        else:
            passages = self.retrieve(query, k)
        
        if not passages:
            return "No relevant information found."
        
        # Format as context
        context = "RELEVANT INFORMATION:\n"
        for i, passage in enumerate(passages, 1):
            context += f"{i}. {passage}\n"
        
        return context
    
    # ============================================================================
    # SEARCH STATISTICS
    # ============================================================================
    
    def get_search_stats(self) -> Dict:
        """
        Get statistics about indexed passages
        
        Returns:
            Statistics dictionary
        """
        return {
            'total_passages': len(self.passages),
            'total_books': len(self.book_passages),
            'average_passages_per_book': len(self.passages) / len(self.book_passages) if self.book_passages else 0,
            'embedding_model': EMBEDDING_MODEL,
            'embedding_dimension': EMBEDDING_DIM
        }
    
    # ============================================================================
    # REFRESH INDEX
    # ============================================================================
    
    def refresh(self):
        """Refresh all passages from database"""
        self._initialize_passages()
    
    # ============================================================================
    # SIMILARITY CALCULATION
    # ============================================================================
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0-1)
        """
        try:
            embedding1 = self.embedding_model.encode(text1, convert_to_tensor=False)
            embedding2 = self.embedding_model.encode(text2, convert_to_tensor=False)
            
            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity(
                [embedding1], 
                [embedding2]
            )[0][0]
            
            return float(similarity)
        
        except Exception as e:
            print(f"⚠️ Similarity calculation error: {e}")
            return 0.0
    
    # ============================================================================
    # QUESTION ANSWERING
    # ============================================================================
    
    def answer_question(self, question: str, book_id: int = None, k: int = 5) -> Dict:
        """
        Answer a question using RAG
        
        Args:
            question: User's question
            book_id: Specific book (optional)
            k: Number of relevant passages
        
        Returns:
            Dictionary with question and context
        """
        
        # Retrieve relevant passages
        if book_id:
            passages = self.retrieve_by_book(question, book_id, k)
        else:
            passages = self.retrieve(question, k)
        
        return {
            'question': question,
            'relevant_passages': passages,
            'passage_count': len(passages),
            'context': self.build_context(question, book_id, k)
        }
    
    # ============================================================================
    # BATCH RETRIEVAL
    # ============================================================================
    
    def retrieve_batch(self, queries: List[str], k: int = 5) -> List[List[str]]:
        """
        Retrieve passages for multiple queries
        
        Args:
            queries: List of queries
            k: Number of passages per query
        
        Returns:
            List of passage lists
        """
        results = []
        for query in queries:
            results.append(self.retrieve(query, k))
        return results