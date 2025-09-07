"""
ProductDataService 단위 테스트
"""

import pytest
import json
import tempfile
import os
from unittest.mock import patch, mock_open
from app.services.product_data_service import ProductDataService
from app.models.product import Product, Review, SellerResponse

class TestProductDataService:
    
    @pytest.fixture
    def sample_product_data(self):
        """테스트용 샘플 제품 데이터"""
        return {
            "products": [
                {
                    "id": "PROD-001",
                    "name": "테스트 제품",
                    "category": "전자제품",
                    "seller_id": "SELLER-001",
                    "price": 50000,
                    "description": "테스트 제품입니다",
                    "image_url": "/images/test.jpg",
                    "features": ["기능1", "기능2"],
                    "reviews": [
                        {
                            "id": "REV-001",
                            "user_name": "테스트유저1",
                            "rating": 5,
                            "content": "좋은 제품입니다",
                            "date": "2024-01-01",
                            "verified_purchase": True
                        },
                        {
                            "id": "REV-002",
                            "user_name": "테스트유저2",
                            "rating": 3,
                            "content": "보통입니다",
                            "date": "2024-01-02",
                            "verified_purchase": True
                        }
                    ]
                }
            ]
        }
    
    @pytest.fixture
    def service(self):
        """ProductDataService 인스턴스"""
        return ProductDataService()
    
    def test_calculate_average_rating(self, service):
        """평균 평점 계산 테스트"""
        reviews = [
            Review(id="1", user_name="user1", rating=5, content="great", date="2024-01-01", verified_purchase=True),
            Review(id="2", user_name="user2", rating=3, content="ok", date="2024-01-02", verified_purchase=True),
            Review(id="3", user_name="user3", rating=4, content="good", date="2024-01-03", verified_purchase=True)
        ]
        
        average = service._calculate_average_rating(reviews)
        assert average == 4.0  # (5 + 3 + 4) / 3 = 4.0
    
    def test_calculate_average_rating_empty_reviews(self, service):
        """빈 리뷰 목록에 대한 평균 평점 계산"""
        average = service._calculate_average_rating([])
        assert average == 0.0
    
    def test_calculate_average_rating_invalid_ratings(self, service):
        """유효하지 않은 평점이 포함된 경우"""
        reviews = [
            Review(id="1", user_name="user1", rating=5, content="great", date="2024-01-01", verified_purchase=True),
            Review(id="2", user_name="user2", rating=None, content="no rating", date="2024-01-02", verified_purchase=True),
            Review(id="3", user_name="user3", rating=4, content="good", date="2024-01-03", verified_purchase=True)
        ]
        
        average = service._calculate_average_rating(reviews)
        assert average == 4.5  # (5 + 4) / 2 = 4.5
    
    def test_calculate_rating_distribution(self, service):
        """평점 분포 계산 테스트"""
        reviews = [
            Review(id="1", user_name="user1", rating=5, content="great", date="2024-01-01", verified_purchase=True),
            Review(id="2", user_name="user2", rating=5, content="excellent", date="2024-01-02", verified_purchase=True),
            Review(id="3", user_name="user3", rating=4, content="good", date="2024-01-03", verified_purchase=True),
            Review(id="4", user_name="user4", rating=3, content="ok", date="2024-01-04", verified_purchase=True),
            Review(id="5", user_name="user5", rating=1, content="bad", date="2024-01-05", verified_purchase=True)
        ]
        
        distribution = service._calculate_rating_distribution(reviews)
        expected = {1: 1, 2: 0, 3: 1, 4: 1, 5: 2}
        assert distribution == expected
    
    def test_calculate_rating_distribution_empty_reviews(self, service):
        """빈 리뷰 목록에 대한 평점 분포"""
        distribution = service._calculate_rating_distribution([])
        expected = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        assert distribution == expected
    
    def test_validate_product_data_valid(self, service):
        """유효한 제품 데이터 검증"""
        valid_data = {
            "id": "PROD-001",
            "name": "테스트 제품",
            "category": "전자제품",
            "price": 50000
        }
        
        assert service._validate_product_data(valid_data) is True
    
    def test_validate_product_data_missing_required_field(self, service):
        """필수 필드 누락된 제품 데이터"""
        invalid_data = {
            "id": "PROD-001",
            "name": "테스트 제품",
            # category 누락
            "price": 50000
        }
        
        assert service._validate_product_data(invalid_data) is False
    
    def test_validate_product_data_invalid_price_type(self, service):
        """잘못된 가격 타입"""
        invalid_data = {
            "id": "PROD-001",
            "name": "테스트 제품",
            "category": "전자제품",
            "price": "50000"  # 문자열 (숫자여야 함)
        }
        
        assert service._validate_product_data(invalid_data) is False
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_raw_data_success(self, mock_json_load, mock_file, service, sample_product_data):
        """JSON 파일 로드 성공 테스트"""
        mock_json_load.return_value = sample_product_data
        
        result = service._load_raw_data()
        assert result == sample_product_data
        mock_file.assert_called_once()
        mock_json_load.assert_called_once()
    
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_raw_data_file_not_found(self, mock_file, service):
        """파일을 찾을 수 없는 경우"""
        result = service._load_raw_data()
        assert result == {"products": []}
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError("Invalid JSON", "", 0))
    def test_load_raw_data_invalid_json(self, mock_json_load, mock_file, service):
        """잘못된 JSON 형식"""
        result = service._load_raw_data()
        assert result == {"products": []}
    
    def test_enhance_product_data(self, service, sample_product_data):
        """제품 데이터 향상 테스트"""
        product_data = sample_product_data["products"][0]
        enhanced = service._enhance_product_data(product_data)
        
        assert "average_rating" in enhanced
        assert "review_count" in enhanced
        assert "rating_distribution" in enhanced
        assert enhanced["average_rating"] == 4.0  # (5 + 3) / 2
        assert enhanced["review_count"] == 2
        assert enhanced["rating_distribution"] == {1: 0, 2: 0, 3: 1, 4: 0, 5: 1}
    
    def test_enhance_product_data_no_reviews(self, service):
        """리뷰가 없는 제품 데이터"""
        product_data = {
            "id": "PROD-001",
            "name": "테스트 제품",
            "category": "전자제품",
            "seller_id": "SELLER-001",
            "price": 50000,
            "description": "테스트 제품입니다",
            "image_url": "/images/test.jpg",
            "features": ["기능1", "기능2"],
            "reviews": []
        }
        
        enhanced = service._enhance_product_data(product_data)
        
        assert enhanced["average_rating"] == 0.0
        assert enhanced["review_count"] == 0
        assert enhanced["rating_distribution"] == {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    @patch.object(ProductDataService, '_load_raw_data')
    def test_load_all_products_success(self, mock_load_raw_data, service, sample_product_data):
        """모든 제품 로드 성공 테스트"""
        mock_load_raw_data.return_value = sample_product_data
        
        products = service.load_all_products()
        
        assert len(products) == 1
        assert isinstance(products[0], Product)
        assert products[0].id == "PROD-001"
        assert products[0].average_rating == 4.0
        assert products[0].review_count == 2
    
    @patch.object(ProductDataService, '_load_raw_data')
    def test_load_all_products_with_cache(self, mock_load_raw_data, service, sample_product_data):
        """캐시를 사용한 제품 로드 테스트"""
        mock_load_raw_data.return_value = sample_product_data
        
        # 첫 번째 호출
        products1 = service.load_all_products()
        
        # 두 번째 호출 (캐시 사용)
        products2 = service.load_all_products()
        
        # _load_raw_data는 한 번만 호출되어야 함
        mock_load_raw_data.assert_called_once()
        assert products1 == products2
    
    @patch.object(ProductDataService, '_load_raw_data')
    def test_load_all_products_force_reload(self, mock_load_raw_data, service, sample_product_data):
        """강제 리로드 테스트"""
        mock_load_raw_data.return_value = sample_product_data
        
        # 첫 번째 호출
        service.load_all_products()
        
        # 강제 리로드
        service.load_all_products(force_reload=True)
        
        # _load_raw_data가 두 번 호출되어야 함
        assert mock_load_raw_data.call_count == 2
    
    @patch.object(ProductDataService, 'load_all_products')
    def test_get_product_by_id_found(self, mock_load_all_products, service):
        """ID로 제품 조회 - 찾은 경우"""
        mock_product = Product(
            id="PROD-001",
            name="테스트 제품",
            category="전자제품",
            seller_id="SELLER-001",
            price=50000,
            description="테스트",
            image_url="/test.jpg",
            features=["기능1"],
            reviews=[]
        )
        mock_load_all_products.return_value = [mock_product]
        
        result = service.get_product_by_id("PROD-001")
        assert result == mock_product
    
    @patch.object(ProductDataService, 'load_all_products')
    def test_get_product_by_id_not_found(self, mock_load_all_products, service):
        """ID로 제품 조회 - 찾지 못한 경우"""
        mock_load_all_products.return_value = []
        
        result = service.get_product_by_id("NONEXISTENT")
        assert result is None
    
    def test_get_product_summary(self, service):
        """제품 요약 정보 조회 테스트"""
        mock_product = Product(
            id="PROD-001",
            name="테스트 제품",
            category="전자제품",
            seller_id="SELLER-001",
            price=50000,
            description="테스트",
            image_url="/test.jpg",
            features=["기능1"],
            reviews=[],
            average_rating=4.5,
            review_count=10
        )
        
        with patch.object(service, 'get_product_by_id', return_value=mock_product):
            summary = service.get_product_summary("PROD-001")
            
            assert summary is not None
            assert summary["id"] == "PROD-001"
            assert summary["name"] == "테스트 제품"
            assert summary["average_rating"] == 4.5
            assert summary["review_count"] == 10
            assert summary["emoji"] == "🎧"  # PROD-001의 기본 이모지
    
    def test_get_product_summary_not_found(self, service):
        """존재하지 않는 제품의 요약 정보 조회"""
        with patch.object(service, 'get_product_by_id', return_value=None):
            summary = service.get_product_summary("NONEXISTENT")
            assert summary is None