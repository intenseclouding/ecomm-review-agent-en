"""
Product Data Service - 제품 데이터 중앙 관리 서비스
JSON 파일에서 데이터를 로드하고 평점 계산 등의 비즈니스 로직을 처리합니다.
"""

import json
import os
from typing import List, Dict, Optional, Any
from statistics import mean
import logging
from ..models.product import Product, Review

logger = logging.getLogger(__name__)

class ProductDataService:
    """제품 데이터 관리를 위한 중앙화된 서비스"""
    
    def __init__(self):
        self._products_cache: Optional[List[Product]] = None
        self._data_file_path = self._get_data_file_path()
    
    def _get_data_file_path(self) -> str:
        """데이터 파일 경로 반환"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..', '..', '..')
        return os.path.join(project_root, 'data', 'sample_products.json')
    
    def _load_raw_data(self) -> Dict[str, Any]:
        """JSON 파일에서 원시 데이터 로드"""
        try:
            with open(self._data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Successfully loaded product data from {self._data_file_path}")
                return data
        except FileNotFoundError:
            logger.error(f"Product data file not found: {self._data_file_path}")
            return {"products": []}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in product data file: {e}")
            return {"products": []}
        except Exception as e:
            logger.error(f"Unexpected error loading product data: {e}")
            return {"products": []}
    
    def _calculate_average_rating(self, reviews: List[Review]) -> float:
        """리뷰 목록에서 평균 평점 계산"""
        if not reviews:
            return 0.0
        
        ratings = [review.rating for review in reviews if review.rating is not None]
        if not ratings:
            return 0.0
        
        return round(mean(ratings), 1)
    
    def _calculate_rating_distribution(self, reviews: List[Review]) -> Dict[int, int]:
        """평점 분포 계산 (1-5점 각각의 개수)"""
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for review in reviews:
            if review.rating and 1 <= review.rating <= 5:
                distribution[review.rating] += 1
        
        return distribution
    
    def _enhance_product_data(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """제품 데이터에 계산된 필드 추가"""
        try:
            # Review 객체 생성
            reviews = []
            for review_data in product_data.get('reviews', []):
                try:
                    review = Review(**review_data)
                    reviews.append(review)
                except Exception as e:
                    logger.warning(f"Invalid review data in product {product_data.get('id', 'unknown')}: {e}")
                    continue
            
            # Return reviews in reverse order (latest first)
            # reviews.sort(lambda x: x.analysis_timestamp, reverse=True)
            
            reviews = [r for r in reviews if r.analysis_completed]
            reviews.sort(key=lambda x: x.analysis_timestamp, reverse=True)
            
            # 계산된 필드 추가
            enhanced_data = product_data.copy()
            enhanced_data['reviews'] = reviews
            enhanced_data['average_rating'] = self._calculate_average_rating(reviews)
            enhanced_data['review_count'] = len(reviews)
            enhanced_data['rating_distribution'] = self._calculate_rating_distribution(reviews)
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error enhancing product data for {product_data.get('id', 'unknown')}: {e}")
            # 기본값으로 fallback
            enhanced_data = product_data.copy()
            enhanced_data['average_rating'] = 0.0
            enhanced_data['review_count'] = 0
            enhanced_data['rating_distribution'] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            return enhanced_data
    
    def _validate_product_data(self, product_data: Dict[str, Any]) -> bool:
        """제품 데이터 유효성 검증"""
        required_fields = ['id', 'name', 'category', 'price']
        
        for field in required_fields:
            if field not in product_data:
                logger.warning(f"Missing required field '{field}' in product data")
                return False
        
        # 가격이 숫자인지 확인
        if not isinstance(product_data.get('price'), (int, float)):
            logger.warning(f"Invalid price type in product {product_data.get('id')}")
            return False
        
        return True
    
    def load_all_products(self, force_reload: bool = True) -> List[Product]:
        """모든 제품 데이터 로드 (캐싱 지원)"""
        if self._products_cache is not None and not force_reload:
            return self._products_cache
        
        try:
            raw_data = self._load_raw_data()
            products = []
            
            for product_data in raw_data.get('products', []):
                if not self._validate_product_data(product_data):
                    continue
                
                try:
                    enhanced_data = self._enhance_product_data(product_data)
                    product = Product(**enhanced_data)
                    products.append(product)
                except Exception as e:
                    logger.error(f"Error creating Product object for {product_data.get('id', 'unknown')}: {e}")
                    continue
            
            self._products_cache = products
            logger.info(f"Successfully loaded {len(products)} products")
            return products
            
        except Exception as e:
            logger.error(f"Critical error loading products: {e}")
            return []
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """ID로 특정 제품 조회"""
        products = self.load_all_products()
        
        for product in products:
            if product.id == product_id:
                return product
        
        logger.warning(f"Product not found: {product_id}")
        return None
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """카테고리별 제품 조회"""
        products = self.load_all_products()
        return [p for p in products if p.category.lower() == category.lower()]
    
    def get_products_by_seller(self, seller_id: str) -> List[Product]:
        """셀러별 제품 조회"""
        products = self.load_all_products()
        return [p for p in products if p.seller_id == seller_id]
    
    def get_product_summary(self, product_id: str) -> Optional[Dict[str, Any]]:
        """제품 요약 정보 반환 (사이드바, 홈페이지용)"""
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        
        # 제품별 이모지 매핑
        emoji_map = {
            'PROD-001': '🎧',
            'PROD-002': '👕', 
            'PROD-003': '✨',
            'PROD-004': '⌚',
            'PROD-005': '🧥'
        }
        
        return {
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'price': product.price,
            'average_rating': product.average_rating,
            'review_count': product.review_count,
            'image_url': product.image_url,
            'emoji': emoji_map.get(product.id, '📦')
        }
    
    def get_all_product_summaries(self) -> List[Dict[str, Any]]:
        """모든 제품의 요약 정보 반환"""
        products = self.load_all_products()
        summaries = []
        
        for product in products:
            summary = self.get_product_summary(product.id)
            if summary:
                summaries.append(summary)
        
        return summaries
    
    def save_products(self, products: List[Product]) -> bool:
        """제품 데이터 저장 (향후 리뷰 추가 등을 위해)"""
        try:
            data = {"products": [product.model_dump() for product in products]}
            
            with open(self._data_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 캐시 무효화
            self._products_cache = None
            logger.info(f"Successfully saved {len(products)} products")
            return True
            
        except Exception as e:
            logger.error(f"Error saving products: {e}")
            return False

# 싱글톤 인스턴스
product_data_service = ProductDataService()