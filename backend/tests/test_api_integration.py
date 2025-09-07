"""
API 엔드포인트 통합 테스트
데이터 일관성 및 API 응답 구조 검증
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models.product import Product, Review
from app.services.product_data_service import ProductDataService

client = TestClient(app)

class TestProductAPIIntegration:
    
    @pytest.fixture
    def mock_products(self):
        """테스트용 제품 데이터"""
        return [
            Product(
                id="PROD-001",
                name="테스트 제품 1",
                category="전자제품",
                seller_id="SELLER-001",
                price=50000,
                description="테스트 제품 1 설명",
                image_url="/test1.jpg",
                features=["기능1", "기능2"],
                reviews=[
                    Review(
                        id="REV-001",
                        user_name="사용자1",
                        rating=5,
                        content="훌륭합니다",
                        date="2024-01-01",
                        verified_purchase=True
                    ),
                    Review(
                        id="REV-002",
                        user_name="사용자2",
                        rating=3,
                        content="보통입니다",
                        date="2024-01-02",
                        verified_purchase=True
                    )
                ],
                average_rating=4.0,
                review_count=2,
                rating_distribution={1: 0, 2: 0, 3: 1, 4: 0, 5: 1}
            ),
            Product(
                id="PROD-002",
                name="테스트 제품 2",
                category="패션",
                seller_id="SELLER-002",
                price=30000,
                description="테스트 제품 2 설명",
                image_url="/test2.jpg",
                features=["기능A", "기능B"],
                reviews=[],
                average_rating=0.0,
                review_count=0,
                rating_distribution={1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            )
        ]
    
    @patch.object(ProductDataService, 'load_all_products')
    def test_get_all_products_consistency(self, mock_load_all_products, mock_products):
        """전체 제품 목록 API 일관성 테스트"""
        mock_load_all_products.return_value = mock_products
        
        response = client.get("/api/products")
        
        assert response.status_code == 200
        data = response.json()
        
        # 응답 구조 검증
        assert isinstance(data, list)
        assert len(data) == 2
        
        # 첫 번째 제품 데이터 검증
        product1 = data[0]
        assert product1["id"] == "PROD-001"
        assert product1["name"] == "테스트 제품 1"
        assert product1["average_rating"] == 4.0
        assert product1["review_count"] == 2
        assert "rating_distribution" in product1
        
        # 두 번째 제품 (리뷰 없음) 데이터 검증
        product2 = data[1]
        assert product2["id"] == "PROD-002"
        assert product2["average_rating"] == 0.0
        assert product2["review_count"] == 0
    
    @patch.object(ProductDataService, 'get_product_by_id')
    def test_get_product_detail_consistency(self, mock_get_product_by_id, mock_products):
        """제품 상세 정보 API 일관성 테스트"""
        mock_get_product_by_id.return_value = mock_products[0]
        
        response = client.get("/api/products/PROD-001")
        
        assert response.status_code == 200
        data = response.json()
        
        # 기본 정보 검증
        assert data["id"] == "PROD-001"
        assert data["name"] == "테스트 제품 1"
        assert data["average_rating"] == 4.0
        assert data["review_count"] == 2
        
        # 리뷰 데이터 검증
        assert len(data["reviews"]) == 2
        assert data["reviews"][0]["rating"] == 5
        assert data["reviews"][1]["rating"] == 3
        
        # 평점 분포 검증
        assert data["rating_distribution"]["1"] == 0
        assert data["rating_distribution"]["3"] == 1
        assert data["rating_distribution"]["5"] == 1
    
    @patch.object(ProductDataService, 'get_product_by_id')
    def test_get_product_not_found(self, mock_get_product_by_id):
        """존재하지 않는 제품 조회 테스트"""
        mock_get_product_by_id.return_value = None
        
        response = client.get("/api/products/NONEXISTENT")
        
        assert response.status_code == 404
        assert "Product not found" in response.json()["detail"]
    
    @patch.object(ProductDataService, 'get_all_product_summaries')
    def test_get_product_summaries_consistency(self, mock_get_all_product_summaries):
        """제품 요약 정보 API 일관성 테스트"""
        mock_summaries = [
            {
                "id": "PROD-001",
                "name": "테스트 제품 1",
                "category": "전자제품",
                "price": 50000,
                "average_rating": 4.0,
                "review_count": 2,
                "image_url": "/test1.jpg",
                "emoji": "🎧"
            },
            {
                "id": "PROD-002",
                "name": "테스트 제품 2",
                "category": "패션",
                "price": 30000,
                "average_rating": 0.0,
                "review_count": 0,
                "image_url": "/test2.jpg",
                "emoji": "👕"
            }
        ]
        mock_get_all_product_summaries.return_value = mock_summaries
        
        response = client.get("/api/products/summaries")
        
        assert response.status_code == 200
        data = response.json()
        
        # 응답 구조 검증
        assert isinstance(data, list)
        assert len(data) == 2
        
        # 요약 정보 필드 검증
        for summary in data:
            assert "id" in summary
            assert "name" in summary
            assert "category" in summary
            assert "price" in summary
            assert "average_rating" in summary
            assert "review_count" in summary
            assert "emoji" in summary
    
    @patch.object(ProductDataService, 'get_products_by_category')
    def test_get_products_by_category_consistency(self, mock_get_products_by_category, mock_products):
        """카테고리별 제품 조회 일관성 테스트"""
        electronics_products = [p for p in mock_products if p.category == "전자제품"]
        mock_get_products_by_category.return_value = electronics_products
        
        response = client.get("/api/products/category/전자제품")
        
        assert response.status_code == 200
        data = response.json()
        
        # 카테고리 필터링 검증
        assert len(data) == 1
        assert data[0]["category"] == "전자제품"
        assert data[0]["id"] == "PROD-001"
    
    @patch.object(ProductDataService, 'get_products_by_seller')
    def test_get_products_by_seller_consistency(self, mock_get_products_by_seller, mock_products):
        """셀러별 제품 조회 일관성 테스트"""
        seller_products = [p for p in mock_products if p.seller_id == "SELLER-001"]
        mock_get_products_by_seller.return_value = seller_products
        
        response = client.get("/api/products/seller/SELLER-001")
        
        assert response.status_code == 200
        data = response.json()
        
        # 셀러 필터링 검증
        assert len(data) == 1
        assert data[0]["seller_id"] == "SELLER-001"
        assert data[0]["id"] == "PROD-001"
    
    def test_api_error_handling_consistency(self):
        """API 에러 처리 일관성 테스트"""
        with patch.object(ProductDataService, 'load_all_products', side_effect=Exception("Database error")):
            response = client.get("/api/products")
            
            assert response.status_code == 500
            assert "Internal server error" in response.json()["detail"]
        
        with patch.object(ProductDataService, 'get_product_by_id', side_effect=Exception("Database error")):
            response = client.get("/api/products/PROD-001")
            
            assert response.status_code == 500
            assert "Internal server error" in response.json()["detail"]
    
    @patch.object(ProductDataService, 'load_all_products')
    @patch.object(ProductDataService, 'get_product_by_id')
    def test_cross_endpoint_data_consistency(self, mock_get_product_by_id, mock_load_all_products, mock_products):
        """엔드포인트 간 데이터 일관성 테스트"""
        mock_load_all_products.return_value = mock_products
        mock_get_product_by_id.return_value = mock_products[0]
        
        # 전체 제품 목록에서 특정 제품 찾기
        all_products_response = client.get("/api/products")
        all_products = all_products_response.json()
        product_from_list = next(p for p in all_products if p["id"] == "PROD-001")
        
        # 개별 제품 상세 정보 가져오기
        detail_response = client.get("/api/products/PROD-001")
        product_detail = detail_response.json()
        
        # 공통 필드들이 일치해야 함
        assert product_from_list["id"] == product_detail["id"]
        assert product_from_list["name"] == product_detail["name"]
        assert product_from_list["category"] == product_detail["category"]
        assert product_from_list["price"] == product_detail["price"]
        assert product_from_list["average_rating"] == product_detail["average_rating"]
        assert product_from_list["review_count"] == product_detail["review_count"]
    
    @patch.object(ProductDataService, 'get_product_summary')
    @patch.object(ProductDataService, 'get_product_by_id')
    def test_summary_vs_detail_consistency(self, mock_get_product_by_id, mock_get_product_summary, mock_products):
        """요약 정보와 상세 정보 간 일관성 테스트"""
        product = mock_products[0]
        mock_get_product_by_id.return_value = product
        mock_get_product_summary.return_value = {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "average_rating": product.average_rating,
            "review_count": product.review_count,
            "image_url": product.image_url,
            "emoji": "🎧"
        }
        
        # 요약 정보 가져오기
        summary_response = client.get("/api/products/PROD-001/summary")
        summary = summary_response.json()
        
        # 상세 정보 가져오기
        detail_response = client.get("/api/products/PROD-001")
        detail = detail_response.json()
        
        # 공통 필드 일치 검증
        assert summary["id"] == detail["id"]
        assert summary["name"] == detail["name"]
        assert summary["category"] == detail["category"]
        assert summary["price"] == detail["price"]
        assert summary["average_rating"] == detail["average_rating"]
        assert summary["review_count"] == detail["review_count"]
    
    @patch.object(ProductDataService, 'load_all_products')
    def test_rating_calculation_consistency(self, mock_load_all_products, mock_products):
        """평점 계산 일관성 테스트"""
        mock_load_all_products.return_value = mock_products
        
        response = client.get("/api/products")
        products = response.json()
        
        for product in products:
            # 평점이 0-5 범위 내에 있어야 함
            assert 0 <= product["average_rating"] <= 5
            
            # 리뷰 개수가 음수가 아니어야 함
            assert product["review_count"] >= 0
            
            # 평점 분포의 합이 리뷰 개수와 일치해야 함
            distribution_sum = sum(product["rating_distribution"].values())
            assert distribution_sum == product["review_count"]
            
            # 리뷰가 없으면 평점이 0이어야 함
            if product["review_count"] == 0:
                assert product["average_rating"] == 0.0
    
    def test_api_response_structure_consistency(self):
        """API 응답 구조 일관성 테스트"""
        with patch.object(ProductDataService, 'load_all_products', return_value=[]):
            # 빈 결과도 올바른 구조를 가져야 함
            response = client.get("/api/products")
            assert response.status_code == 200
            assert isinstance(response.json(), list)
        
        with patch.object(ProductDataService, 'get_all_product_summaries', return_value=[]):
            response = client.get("/api/products/summaries")
            assert response.status_code == 200
            assert isinstance(response.json(), list)
        
        with patch.object(ProductDataService, 'get_products_by_category', return_value=[]):
            response = client.get("/api/products/category/nonexistent")
            assert response.status_code == 200
            assert isinstance(response.json(), list)