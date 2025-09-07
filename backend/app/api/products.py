from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging
from ..models.product import Product, Review, ReviewCreate
from ..services.product_data_service import product_data_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/products", response_model=List[Product])
async def get_products():
    """모든 제품 목록 조회"""
    try:
        products = product_data_service.load_all_products()
        logger.info(f"Retrieved {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving products")

@router.get("/products/summaries", response_model=List[Dict[str, Any]])
async def get_product_summaries():
    """모든 제품의 요약 정보 조회 (홈페이지, 사이드바용)"""
    try:
        summaries = product_data_service.get_all_product_summaries()
        logger.info(f"Retrieved {len(summaries)} product summaries")
        return summaries
    except Exception as e:
        logger.error(f"Error retrieving product summaries: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving product summaries")

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """특정 제품 상세 조회"""
    try:
        product = product_data_service.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product not found: {product_id}")
        
        logger.info(f"Retrieved product: {product_id}")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving product")

@router.get("/products/category/{category}", response_model=List[Product])
async def get_products_by_category(category: str):
    """카테고리별 제품 조회"""
    try:
        products = product_data_service.get_products_by_category(category)
        logger.info(f"Retrieved {len(products)} products for category: {category}")
        return products
    except Exception as e:
        logger.error(f"Error retrieving products for category {category}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving products by category")

@router.get("/products/seller/{seller_id}", response_model=List[Product])
async def get_products_by_seller(seller_id: str):
    """셀러별 제품 조회"""
    try:
        products = product_data_service.get_products_by_seller(seller_id)
        logger.info(f"Retrieved {len(products)} products for seller: {seller_id}")
        return products
    except Exception as e:
        logger.error(f"Error retrieving products for seller {seller_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving products by seller")

@router.get("/products/{product_id}/summary", response_model=Dict[str, Any])
async def get_product_summary(product_id: str):
    """특정 제품의 요약 정보 조회"""
    try:
        summary = product_data_service.get_product_summary(product_id)
        if not summary:
            raise HTTPException(status_code=404, detail=f"Product not found: {product_id}")
        
        logger.info(f"Retrieved summary for product: {product_id}")
        return summary
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving summary for product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving product summary")