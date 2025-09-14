import sqlite3
import json
import os
from typing import List, Dict, Optional, Any
from statistics import mean
import logging
from ..models.product import Product, Review, MediaFile, SellerResponse

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self._db_path = self._get_db_path()
        self._products_cache: Optional[List[Product]] = None
    
    def _get_db_path(self) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..', '..', '..')
        return os.path.join(project_root, 'ecommerce_reviews.db')
    
    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _safe_get(self, row, key, default=None):
        """sqlite3.Row에서 안전하게 값을 가져오는 헬퍼 메서드"""
        try:
            return row[key] if key in row.keys() else default
        except (KeyError, IndexError):
            return default
    
    def _calculate_average_rating(self, reviews: List[Review]) -> float:
        if not reviews:
            return 0.0
        ratings = [r.rating for r in reviews if r.rating is not None]
        return round(mean(ratings), 1) if ratings else 0.0
    
    def _calculate_rating_distribution(self, reviews: List[Review]) -> Dict[int, int]:
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for review in reviews:
            if review.rating and 1 <= review.rating <= 5:
                distribution[review.rating] += 1
        return distribution
    
    def load_all_products(self, force_reload: bool = True) -> List[Product]:
        if self._products_cache is not None and not force_reload:
            return self._products_cache
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM products")
            product_rows = cursor.fetchall()
            
            products = []
            for row in product_rows:
                # Load reviews for this product
                reviews = self._load_reviews_for_product(cursor, row['id'])
                
                product_data = {
                    'id': row['id'],
                    'name': row['name'],
                    'category': row['category'],
                    'seller_id': row['seller_id'],
                    'price': row['price'],
                    'description': row['description'],
                    'image_url': row['image_url'],
                    'features': json.loads(row['features']) if row['features'] else [],
                    'reviews': reviews,
                    'average_rating': self._calculate_average_rating(reviews),
                    'review_count': len(reviews),
                    'rating_distribution': self._calculate_rating_distribution(reviews)
                }
                
                products.append(Product(**product_data))
            
            conn.close()
            self._products_cache = products
            return products
            
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            return []
    
    def _load_reviews_for_product(self, cursor: sqlite3.Cursor, product_id: str) -> List[Review]:
        cursor.execute("SELECT * FROM reviews WHERE product_id = ?", (product_id,))
        review_rows = cursor.fetchall()
        
        reviews = []
        for row in review_rows:
            # Load seller response
            seller_response = None
            cursor.execute("SELECT * FROM seller_responses WHERE review_id = ?", (row['id'],))
            seller_row = cursor.fetchone()
            if seller_row:
                seller_response = SellerResponse(
                    content=seller_row['content'],
                    date=seller_row['date']
                )
            
            # Load media files
            media_files = []
            cursor.execute("SELECT * FROM media_files WHERE review_id = ?", (row['id'],))
            media_rows = cursor.fetchall()
            for media_row in media_rows:
                media_files.append(MediaFile(
                    id=media_row['id'],
                    type=media_row['type'],
                    url=media_row['url'],
                    filename=media_row['filename'],
                    size=media_row['size'],
                    thumbnail_url=media_row['thumbnail_url']
                ))
            
            review_data = {
                'id': row['id'],
                'user_name': row['user_name'],
                'rating': row['rating'],
                'content': row['content'],
                'date': row['date'],
                'verified_purchase': bool(row['verified_purchase']),
                'auto_response': row['auto_response'],
                'response_approved': bool(row['response_approved']),
                'keywords': json.loads(row['keywords']) if row['keywords'] else None,
                'sentiment': json.loads(row['sentiment']) if row['sentiment'] else None,
                'analysis_completed': bool(row['analysis_completed']),
                'analysis_timestamp': row['analysis_timestamp'],
                'moderation_status': self._safe_get(row, 'moderation_status', 'PENDING'),
                'moderation_results': self._safe_get(row, 'moderation_results'),
                'moderation_timestamp': self._safe_get(row, 'moderation_timestamp'),
                'is_approved': bool(self._safe_get(row, 'is_approved', False)),
                'agent_log_id': row['agent_log_id'],
                'seller_response': seller_response,
                'media_files': media_files if media_files else None
            }
            
            reviews.append(Review(**review_data))
        
        # 승인된 리뷰만 표시 (검수 통과한 리뷰)
        approved_reviews = [r for r in reviews if r.is_approved]
        # 날짜순으로 정렬 (최신순)
        approved_reviews.sort(key=lambda x: x.date, reverse=True)
        return approved_reviews
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        products = self.load_all_products()
        for product in products:
            if product.id == product_id:
                return product
        return None
    
    def add_review(self, product_id: str, review: Review) -> bool:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO reviews 
                (id, product_id, user_name, rating, content, date, verified_purchase,
                 auto_response, response_approved, keywords, sentiment, 
                 analysis_completed, analysis_timestamp, agent_log_id,
                 moderation_status, moderation_results, moderation_timestamp, is_approved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                review.id, product_id, review.user_name, review.rating, review.content,
                review.date, review.verified_purchase, review.auto_response,
                review.response_approved,
                json.dumps(review.keywords) if review.keywords else None,
                json.dumps(review.sentiment) if review.sentiment else None,
                review.analysis_completed, review.analysis_timestamp, review.agent_log_id,
                review.moderation_status, review.moderation_results, 
                review.moderation_timestamp, review.is_approved
            ))
            
            # Add media files if any
            if review.media_files:
                for media in review.media_files:
                    cursor.execute('''
                        INSERT INTO media_files 
                        (id, review_id, type, url, filename, size, thumbnail_url)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (media.id, review.id, media.type, media.url, 
                          media.filename, media.size, media.thumbnail_url))
            
            conn.commit()
            conn.close()
            self._products_cache = None  # Invalidate cache
            return True
            
        except Exception as e:
            logger.error(f"Error adding review: {e}")
            return False

    def update_review(self, review: Review) -> bool:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE reviews SET
                auto_response = ?, response_approved = ?, keywords = ?, sentiment = ?,
                analysis_completed = ?, analysis_timestamp = ?, agent_log_id = ?
                WHERE id = ?
            ''', (
                review.auto_response, review.response_approved,
                json.dumps(review.keywords) if review.keywords else None,
                json.dumps(review.sentiment) if review.sentiment else None,
                review.analysis_completed, review.analysis_timestamp,
                review.agent_log_id, review.id
            ))
            
            conn.commit()
            conn.close()
            self._products_cache = None
            return True
            
        except Exception as e:
            logger.error(f"Error updating review: {e}")
            return False
    
    def get_product_summary(self, product_id: str) -> Optional[Dict[str, Any]]:
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        
        emoji_map = {
            'PROD-001': '🎧', 'PROD-002': '👕', 'PROD-003': '✨',
            'PROD-004': '⌚', 'PROD-005': '🧥'
        }
        
        return {
            'id': product.id, 'name': product.name, 'category': product.category,
            'price': product.price, 'average_rating': product.average_rating,
            'review_count': product.review_count, 'image_url': product.image_url,
            'emoji': emoji_map.get(product.id, '📦')
        }
    
    def get_all_product_summaries(self) -> List[Dict[str, Any]]:
        products = self.load_all_products()
        return [self.get_product_summary(p.id) for p in products if self.get_product_summary(p.id)]
    
    def get_review_by_id(self, review_id: str) -> Optional[Review]:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return None
            
            # Load seller response
            seller_response = None
            cursor.execute("SELECT * FROM seller_responses WHERE review_id = ?", (review_id,))
            seller_row = cursor.fetchone()
            if seller_row:
                seller_response = SellerResponse(
                    content=seller_row['content'],
                    date=seller_row['date']
                )
            
            # Load media files
            media_files = []
            cursor.execute("SELECT * FROM media_files WHERE review_id = ?", (review_id,))
            media_rows = cursor.fetchall()
            for media_row in media_rows:
                media_files.append(MediaFile(
                    id=media_row['id'],
                    type=media_row['type'],
                    url=media_row['url'],
                    filename=media_row['filename'],
                    size=media_row['size'],
                    thumbnail_url=media_row['thumbnail_url']
                ))
            
            review_data = {
                'id': row['id'],
                'user_name': row['user_name'],
                'rating': row['rating'],
                'content': row['content'],
                'date': row['date'],
                'verified_purchase': bool(row['verified_purchase']),
                'auto_response': row['auto_response'],
                'response_approved': bool(row['response_approved']),
                'keywords': json.loads(row['keywords']) if row['keywords'] else None,
                'sentiment': json.loads(row['sentiment']) if row['sentiment'] else None,
                'analysis_completed': bool(row['analysis_completed']),
                'analysis_timestamp': row['analysis_timestamp'],
                'moderation_status': self._safe_get(row, 'moderation_status', 'PENDING'),
                'moderation_results': self._safe_get(row, 'moderation_results'),
                'moderation_timestamp': self._safe_get(row, 'moderation_timestamp'),
                'is_approved': bool(self._safe_get(row, 'is_approved', False)),
                'agent_log_id': row['agent_log_id'],
                'seller_response': seller_response,
                'media_files': media_files if media_files else None
            }
            
            conn.close()
            return Review(**review_data)
            
        except Exception as e:
            logger.error(f"Error getting review by id {review_id}: {e}")
            return None

database_service = DatabaseService()