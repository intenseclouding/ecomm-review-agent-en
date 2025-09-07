from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import json
import uuid
from datetime import datetime
import sys
import os

# agents 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../agents'))

from ..models.product import Product, Review, ReviewCreate, ReviewAnalysisResult, AutoResponseResult, AgentLog
from ..services.product_data_service import product_data_service
from ..services.agent_log_service import load_agent_log_by_id, load_agent_log_by_review_id
from ..services.log_utils import get_log_statistics
from ..services.api_cache import get_cached_log, cache_log, get_cache_stats

router = APIRouter()

def generate_review_id():
    """리뷰 ID 생성"""
    return f"REV-{uuid.uuid4().hex[:8].upper()}"

@router.post("/products/{product_id}/reviews")
async def create_review(
    product_id: str, 
    review_data: ReviewCreate,
    background_tasks: BackgroundTasks
):
    """새 리뷰 작성 - 검수 후 승인된 경우에만 저장"""
    products = product_data_service.load_all_products()
    
    # 제품 찾기
    product = None
    product_index = None
    for i, p in enumerate(products):
        if p.id == product_id:
            product = p
            product_index = i
            break
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # 1. 먼저 리뷰 내용 검수 수행
    try:
        from review_analyzer.agent import moderate_and_analyze_review
        moderation_result = moderate_and_analyze_review(review_data.content, product_id)
        
        # 검수 실패 시 에러 반환 (리뷰 저장하지 않음)
        if not moderation_result["success"] and moderation_result.get("moderation_failed", False):
            moderation_info = moderation_result.get("moderation_result", {})
            raise HTTPException(
                status_code=400, 
                detail={
                    "error": "리뷰 검수 실패",
                    "reason": moderation_info.get("reason", "부적절한 내용이 포함되어 있습니다."),
                    "decision": moderation_info.get("decision", "거부"),
                    "issues": moderation_info.get("issues", []),
                    "severity_score": moderation_info.get("severity_score", 0)
                }
            )
        
        # 2. 검수 통과 시 리뷰 저장
        new_review = Review(
            id=generate_review_id(),
            user_name=review_data.user_name,
            rating=review_data.rating,
            content=review_data.content,
            date=datetime.now().strftime("%Y-%m-%d"),
            verified_purchase=review_data.verified_purchase
        )
        
        # 분석 결과가 있으면 함께 저장
        if moderation_result["success"] and moderation_result.get("structured_data"):
            structured_data = moderation_result["structured_data"]
            structured_data["analysis_timestamp"] = datetime.now().isoformat()
            
            new_review.keywords = structured_data["keywords"]
            new_review.sentiment = structured_data["sentiment"]
            new_review.analysis_completed = structured_data["analysis_completed"]
            new_review.analysis_timestamp = structured_data["analysis_timestamp"]
        
        # 제품에 리뷰 추가
        products[product_index].reviews.append(new_review)
        product_data_service.save_products(products)
        
        # 백그라운드에서 자동 응답 생성 (분석은 이미 완료됨)
        if moderation_result["success"]:
            background_tasks.add_task(
                process_auto_response_only,
                product_id,
                new_review.id,
                moderation_result.get("raw_analysis", {}),
                product.seller_id
            )
        
        return {
            "message": "리뷰가 성공적으로 등록되었습니다.",
            "review_id": new_review.id,
            "status": "검수 통과 - 자동 응답 생성 중...",
            "moderation_passed": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"리뷰 검수 중 오류 발생: {e}")
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "리뷰 처리 중 오류가 발생했습니다.",
                "reason": "시스템 오류",
                "message": str(e)
            }
        )

@router.get("/products/{product_id}/reviews", response_model=List[Review])
async def get_product_reviews(product_id: str):
    """제품의 모든 리뷰 조회"""
    product = product_data_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.reviews

@router.get("/reviews/{review_id}", response_model=Review)
async def get_review(review_id: str):
    """특정 리뷰 조회"""
    products = product_data_service.load_all_products()
    for product in products:
        for review in product.reviews:
            if review.id == review_id:
                return review
    raise HTTPException(status_code=404, detail="Review not found")

@router.post("/reviews/{review_id}/approve-response")
async def approve_auto_response(review_id: str):
    """자동 생성된 댓글 승인"""
    products = product_data_service.load_all_products()
    
    for i, product in enumerate(products):
        for j, review in enumerate(product.reviews):
            if review.id == review_id:
                if review.auto_response:
                    products[i].reviews[j].response_approved = True
                    product_data_service.save_products(products)
                    return {"message": "자동 댓글이 승인되었습니다."}
                else:
                    raise HTTPException(status_code=400, detail="승인할 자동 댓글이 없습니다.")
    
    raise HTTPException(status_code=404, detail="Review not found")

@router.delete("/reviews/{review_id}/response")
async def reject_auto_response(review_id: str):
    """자동 생성된 댓글 거부"""
    products = product_data_service.load_all_products()
    
    for i, product in enumerate(products):
        for j, review in enumerate(product.reviews):
            if review.id == review_id:
                products[i].reviews[j].auto_response = None
                products[i].reviews[j].response_approved = False
                product_data_service.save_products(products)
                return {"message": "자동 댓글이 거부되었습니다."}
    
    raise HTTPException(status_code=404, detail="Review not found")

@router.get("/reviews/{review_id}/agent-log")
async def get_agent_log_by_review(review_id: str):
    """특정 리뷰의 에이전트 로그 조회 (캐싱 적용)"""
    try:
        # 캐시 확인
        cache_key = f"review_log_{review_id}"
        cached_log = get_cached_log(cache_key)
        
        if cached_log:
            return cached_log
        
        # 먼저 리뷰가 존재하는지 확인
        products = product_data_service.load_all_products()
        review_found = False
        
        for product in products:
            for review in product.reviews:
                if review.id == review_id:
                    review_found = True
                    break
            if review_found:
                break
        
        if not review_found:
            raise HTTPException(status_code=404, detail="Review not found")
        
        # 로그 조회
        log = load_agent_log_by_review_id(review_id)
        if not log:
            raise HTTPException(status_code=404, detail="Agent log not found for this review")
        
        # 캐시에 저장
        cache_log(cache_key, log, ttl=600)  # 10분 캐싱
        
        return log
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"로그 조회 중 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/agent-logs/{log_id}")
async def get_agent_log_by_id(log_id: str):
    """로그 ID로 에이전트 로그 조회 (캐싱 적용)"""
    try:
        # 캐시 확인
        cache_key = f"log_{log_id}"
        cached_log = get_cached_log(cache_key)
        
        if cached_log:
            return cached_log
        
        log = load_agent_log_by_id(log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Agent log not found")
        
        # 캐시에 저장
        cache_log(cache_key, log, ttl=600)  # 10분 캐싱
        
        return log
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"로그 조회 중 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_auto_response_only(product_id: str, review_id: str, analysis_data: dict, seller_id: str):
    """자동 응답만 생성하는 함수 (분석은 이미 완료된 상태)"""
    try:
        from auto_responder.agent import create_auto_response
        
        # 자동 응답 생성을 위한 구조화된 분석 데이터 준비
        enhanced_analysis = {
            "review_text": analysis_data.get("review_text", ""),
            "sentiment": analysis_data.get("sentiment", {}),
            "keywords": analysis_data.get("keywords", []),
            "topic_analysis": analysis_data.get("topic_analysis", {}),
            "spam_check": analysis_data.get("spam_check", {})
        }
        
        response_result = create_auto_response(
            review_analysis=enhanced_analysis,
            seller_id=seller_id,
            personalization_level="medium"
        )
        
        if response_result["success"]:
            # 생성된 응답을 데이터베이스에 저장
            products = product_data_service.load_all_products()
            for i, product in enumerate(products):
                for j, review in enumerate(product.reviews):
                    if review.id == review_id:
                        products[i].reviews[j].auto_response = "소중한 리뷰 감사합니다! 더 나은 서비스로 보답하겠습니다."
                        product_data_service.save_products(products)
                        break
        
    except Exception as e:
        print(f"자동 응답 생성 중 오류 발생: {e}")

async def process_review_automation(product_id: str, review_id: str, review_content: str, seller_id: str):
    """리뷰 자동화 처리 (분석 + 자동 응답 생성) - 기존 호환성 유지"""
    try:
        # 새로운 구조화된 리뷰 분석 함수 사용
        from review_analyzer.agent import analyze_review_for_storage
        analysis_result = analyze_review_for_storage(review_content, product_id)
        
        # 분석 결과를 리뷰 데이터에 저장
        products = product_data_service.load_all_products()
        for i, product in enumerate(products):
            for j, review in enumerate(product.reviews):
                if review.id == review_id:
                    if analysis_result["success"]:
                        # 분석 성공 시 구조화된 데이터 저장
                        structured_data = analysis_result["structured_data"]
                        structured_data["analysis_timestamp"] = datetime.now().isoformat()
                        
                        products[i].reviews[j].keywords = structured_data["keywords"]
                        products[i].reviews[j].sentiment = structured_data["sentiment"]
                        products[i].reviews[j].analysis_completed = structured_data["analysis_completed"]
                        products[i].reviews[j].analysis_timestamp = structured_data["analysis_timestamp"]
                    else:
                        # 분석 실패 시 기본값 설정
                        products[i].reviews[j].keywords = []
                        products[i].reviews[j].sentiment = {
                            "label": "중립",
                            "confidence": 0.5,
                            "polarity": 0.0
                        }
                        products[i].reviews[j].analysis_completed = False
                        products[i].reviews[j].analysis_timestamp = datetime.now().isoformat()
                    
                    product_data_service.save_products(products)
                    break
        
        # 자동 응답 생성 (분석 성공 시에만)
        if analysis_result["success"]:
            from auto_responder.agent import create_auto_response
            
            # 분석된 데이터를 자동 응답 생성에 활용
            raw_analysis = analysis_result["raw_analysis"]
            
            # 자동 응답 생성을 위한 구조화된 분석 데이터 준비
            enhanced_analysis = {
                "review_text": review_content,
                "sentiment": raw_analysis["sentiment"],
                "keywords": raw_analysis["keywords"],
                "topic_analysis": raw_analysis["topic_analysis"],
                "spam_check": raw_analysis["spam_check"]
            }
            
            response_result = create_auto_response(
                review_analysis=enhanced_analysis,
                seller_id=seller_id,
                personalization_level="medium"
            )
            
            if response_result["success"]:
                # 생성된 응답을 데이터베이스에 저장
                products = product_data_service.load_all_products()
                for i, product in enumerate(products):
                    for j, review in enumerate(product.reviews):
                        if review.id == review_id:
                            products[i].reviews[j].auto_response = "소중한 리뷰 감사합니다! 더 나은 서비스로 보답하겠습니다."
                            product_data_service.save_products(products)
                            break
        
    except Exception as e:
        print(f"리뷰 자동화 처리 중 오류 발생: {e}")
        # 분석 실패 시에도 기본 데이터는 저장
        try:
            products = product_data_service.load_all_products()
            for i, product in enumerate(products):
                for j, review in enumerate(product.reviews):
                    if review.id == review_id:
                        products[i].reviews[j].keywords = []
                        products[i].reviews[j].sentiment = {
                            "label": "중립",
                            "confidence": 0.5,
                            "polarity": 0.0
                        }
                        products[i].reviews[j].analysis_completed = False
                        products[i].reviews[j].analysis_timestamp = datetime.now().isoformat()
                        product_data_service.save_products(products)
                        break
        except Exception as save_error:
            print(f"기본 데이터 저장 중 오류: {save_error}")

@router.get("/agent-logs/stats")
async def get_agent_log_statistics():
    """에이전트 로그 통계 조회"""
    try:
        stats = get_log_statistics()
        cache_stats = get_cache_stats()
        
        return {
            "success": True,
            "statistics": stats,
            "cache_stats": cache_stats
        }
    except Exception as e:
        print(f"로그 통계 조회 중 오류: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")